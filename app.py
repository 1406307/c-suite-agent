import streamlit as st
import os
from crewai import Agent, Task, Crew, LLM
from crewai.process import Process

# --- 1. CLOUD INFRASTRUCTURE FIXES ---
# These lines prevent ChromaDB from trying to access restricted system files
os.environ['ANONYMIZED_TELEMETRY'] = 'False'
os.environ['CHROMA_SERVER_NOFILE'] = 'True'

# --- 2. SETUP & BRAIN ---
st.set_page_config(page_title="Career Accelerator", layout="wide", page_icon="🚀")

# Priority: Streamlit Secrets -> Environment Variables
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("🔑 Missing Google API Key. Go to Streamlit Settings > Secrets and add: GOOGLE_API_KEY = 'your_key'")
    st.stop()

# Using the 2026 stable Gemini 3 model
gemini_llm = LLM(
    model="gemini/gemini-3-flash-preview",
    api_key=api_key,
    temperature=0.7
)

# --- 3. UI SIDEBAR & PROFILE ---
st.title("🚀 Career Accelerator: C-Suite Path")
st.markdown("---")

with st.sidebar:
    st.header("Executive Profile")
    target_degree = st.selectbox(
        "Target Degree", 
        ["MS in SCM (Supply Chain)", "MBA", "MEM (Engineering Management)"]
    )
    st.divider()
    st.info(f"Currently optimizing your path for a {target_degree} at top-tier US institutions.")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. THE AGENTIC LOOP ---
if prompt := st.chat_input("Ask about universities, leadership, or communication..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Consulting the C-Suite Council..."):
        try:
            # Define the Strategist Agent
            expert = Agent(
                role='Career & Admissions Strategist',
                goal=f'Guide the user toward a {target_degree} at a top US university.',
                backstory=(
                    "You are a top-tier executive consultant. You understand "
                    "the nuances of Ivy League admissions and the leadership "
                    "qualities required to reach the C-suite of an MNC."
                ),
                llm=gemini_llm,
                allow_delegation=False,
                verbose=True
            )

            # Define the specific Task
            consultation_task = Task(
                description=(
                    f"User Inquiry: {prompt}\n"
                    f"Context: The user wants to pursue a {target_degree} in the USA. "
                    "Provide a strategic, executive-level answer with actionable steps."
                ),
                agent=expert,
                expected_output="A structured response with specific recommendations and a 'Leadership Tip' section."
            )

            # Define the Crew with 'Memory=False' to avoid ConfigError
            accelerator_crew = Crew(
                agents=[expert],
                tasks=[consultation_task],
                process=Process.sequential,
                memory=False, # This is the critical fix for ConfigError
                verbose=True
            )

            # Execute the search
            result = accelerator_crew.kickoff()
            
            # Clean and display result
            response = str(result)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)

        except Exception as e:
            st.error(f"An error occurred: {e}")