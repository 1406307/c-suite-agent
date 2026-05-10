import os
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

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

# Agent 1: The Master's Admission Guru
admissions_expert = Agent(
    role='US Admissions Strategist',
    goal='Find top US Master\'s programs that lead to C-suite roles.',
    backstory='You specialize in matching high-potential candidates with Ivy League and top-tier tech universities.',
    llm=gemini_llm
)

# Agent 2: The Executive Coach
leadership_coach = Agent(
    role='Executive Presence Coach',
    goal='Train the user in C-suite level communication.',
    backstory='You analyze speech patterns and leadership philosophy to build world-class executives.',
    lllm=gemini_llm
)

# Define the first mission
task1 = Task(
    description="Research 3 universities in the USA known for strong alumni networks in MNC leadership.",
    agent=admissions_expert,
    expected_output="A summary of 3 schools with specific leadership tracks.",
    human_input=True
)

# Build the Crew
c_suite_crew = Crew(
    agents=[admissions_expert, leadership_coach],
    tasks=[task1],
    verbose=True
)

# Execute!
print("### STARTING C-SUITE ARCHITECT AGENT ###")
result = c_suite_crew.kickoff()
print(result)
