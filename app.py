import streamlit as st
from crewai import Agent, Task, Crew, LLM
# ... import your agents and tasks from main.py ...

st.set_page_config(page_title="Career accelerator", layout="wide")
st.title("Career accelerator")

# Sidebar for profile settings
with st.sidebar:
    st.header("Executive Profile")
    target_degree = st.selectbox("Target Degree", ["MS in SCM", "MBA", "MEM"])
    st.info("I am currently researching Ivy League opportunities for you.")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask about your Master's path..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Trigger your CrewAI logic here
    # result = my_crew.kickoff(inputs={'goal': prompt})
    
    response = "I've analyzed your goal. Let's look at Stanford's leadership tracks."
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)