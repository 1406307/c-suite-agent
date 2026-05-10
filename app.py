import solara
import os
from crewai import Agent, Task, Crew, LLM

# 1. Setup the AI Brain (Infrastructure remains the same)
env_path = Path('.') / '.venv'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found. Check your .env file!")
# Setup Gemini 1.5 Flash (Fast and Free)
gemini_llm = LLM(
    model="gemini/gemini-3-flash-preview",
    google_api_key=api_key,
    temperature=0.7
)

# 2. Reactive State (This is where Solara shines)
user_prompt = solara.reactive("")
chat_history = solara.reactive([])
target_degree = solara.reactive("MBA")

@solara.component
def Page():
    with solara.Column(style={"padding": "20px", "max-width": "800px"}):
        solara.Title("🚀 Career Accelerator: C-Suite Path")
        
        # Sidebar-style settings
        with solara.Card("Executive Profile"):
            solara.Select("Target Degree", value=target_degree, 
                          values=["MS in SCM", "MBA", "MEM"])
            solara.Info(f"Strategizing for {target_degree.value}...")

        # Chat History Display
        for msg in chat_history.value:
            with solara.Row():
                solara.Markdown(f"**{msg['role']}:** {msg['content']}")

        # Chat Input
        solara.InputText("Ask your C-Suite Council...", 
                         value=user_prompt, 
                         on_value=user_prompt.set)
        
        def run_agent():
            # Create Agent
            expert = Agent(
                role='Executive Consultant',
                goal=f'Optimize a {target_degree.value} path.',
                backstory='Specialist in MNC leadership pipelines.',
                llm=gemini_llm
            )
            
            task = Task(description=user_prompt.value, agent=expert, expected_output="A strategic plan.")
            crew = Crew(agents=[expert], tasks=[task], memory=False)
            
            # Execute and update history
            result = str(crew.kickoff())
            new_history = chat_history.value + [
                {"role": "User", "content": user_prompt.value},
                {"role": "AI", "content": result}
            ]
            chat_history.set(new_history)
            user_prompt.set("") # Clear input

        solara.Button("Consult Council", on_click=run_agent, color="primary")