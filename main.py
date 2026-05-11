import os
from crewai import Agent, Task, Crew, LLM
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

def run_persona_agent(user_input, persona_type, target_degree):
    api_key = os.getenv("GOOGLE_API_KEY")
    
    # 1. Setup the Embedding Brain (Turns text into searchable numbers)
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=api_key,
        task_type="retrieval_query",
        client_options={"api_endpoint": "generativelanguage.googleapis.com"}
    )
    gemini_llm = LLM(model="gemini/gemini-2.5-flash", api_key=api_key)
    # 2. Connect to ChromaDB
    # It looks for a folder named 'career_vault' in your project
    vector_db = Chroma(
        persist_directory="./career_vault", 
        embedding_function=embeddings
    )

    # 3. Retrieve Context (The Personalized Part)
    # This searches your CV/Details for the 2 most relevant parts
    search_results = vector_db.similarity_search(user_input, k=2)
    context_from_memory = "\n".join([doc.page_content for doc in search_results])

    # 4. Setup the Persona
    gemini_llm = LLM(model="gemini/gemini-3-flash-preview", api_key=api_key)

    agent = Agent(
        role=f'Executive {persona_type}',
        goal=f'Provide a personalized strategy for a {target_degree} candidate.',
        backstory=(
            "You have access to the user's private career vault (CV and history). "
            "Use this data to ensure every piece of advice is tailored to their specific background."
        ),
        llm=gemini_llm
    )

    # 5. The Personalized Task
    task = Task(
        description=(
            f"User Question: {user_input}\n\n"
            f"Relevant Details from User's CV/History:\n{context_from_memory}\n\n"
            f"Context: Aiming for {target_degree}."
        ),
        agent=agent,
        expected_output="A hyper-personalized response based on the user's actual background."
    )

    crew = Crew(agents=[agent], tasks=[task], memory=False)
    return str(crew.kickoff())