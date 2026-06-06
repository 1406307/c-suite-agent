import os
from crewai import Agent, Task, Crew, LLM
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

def run_persona_agent(user_input, persona_type, target_degree):
    # Grab the Mistral API key from your environment variables
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    
    # 1. Setup the Embedding Brain (Keeping this as Gemini text-embedding-005)
    embeddings = GoogleGenerativeAIEmbeddings(
        model="text-embedding-005",  
        google_api_key=google_api_key,
        task_type="retrieval_query"
    )
    
    # 2. Connect to ChromaDB
    vector_db = Chroma(
        persist_directory="./career_vault", 
        embedding_function=embeddings
    )

    # 3. Retrieve Context
    search_results = vector_db.similarity_search(user_input, k=2)
    context_from_memory = "\n".join([doc.page_content for doc in search_results])

    # 4. Setup the Mistral LLM Configuration
    # You can change "mistral-large-latest" to "open-mixtral-8x22b" or "codestral-latest" depending on your preference
    mistral_llm = LLM(
        model="mistral/mistral-large-latest", 
        api_key=mistral_api_key
    )

    # 5. Assign the Mistral LLM to the Agent
    agent = Agent(
        role=f'Executive {persona_type}',
        goal=f'Provide a personalized strategy for a {target_degree} candidate.',
        backstory=(
            "You have access to the user's private career vault (CV and history). "
            "Use this data to ensure every piece of advice is tailored to their specific background."
        ),
        llm=mistral_llm  # Swapped to Mistral here
    )

    # 6. The Personalized Task
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
