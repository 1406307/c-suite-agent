import os
from crewai import Agent, Task, Crew, LLM

def run_persona_agent(user_input, persona_type, target_degree):
    api_key = os.getenv("GOOGLE_API_KEY")
    gemini_llm = LLM(model="gemini/gemini-3-flash-preview", api_key=api_key)

    # Define the persona profiles
    if persona_type == "Career Expert":
        role = 'Senior Admissions & Career Strategist'
        goal = f'Optimize your path for a {target_degree} and C-suite placement.'
        backstory = 'Former Ivy League admissions officer and MNC recruiter.'
    else: # Chief Communication Officer
        role = 'Executive Communication & IELTS Expert'
        goal = 'Achieve IELTS Band 8.5+ and master executive-level English.'
        backstory = 'Former IELTS Senior Examiner and Fortune 500 speechwriter.'

    # Create the selected Agent
    agent = Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        llm=gemini_llm,
        verbose=True
    )

    # Create the Task
    task = Task(
        description=f"User Request: {user_input}. Context: User is aiming for a {target_degree}.",
        agent=agent,
        expected_output="A concise, high-impact professional response."
    )

    crew = Crew(agents=[agent], tasks=[task], memory=False)
    return str(crew.kickoff())