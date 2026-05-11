import solara
from main import run_persona_agent

# Reactive State
selected_persona = solara.reactive("Career Expert")
user_prompt = solara.reactive("")
chat_history = solara.reactive([])
target_degree = solara.reactive("MS in SCM")

@solara.component
def Page():
    with solara.Column(style={"padding": "30px", "max-width": "800px", "margin": "auto"}):
        solara.Title("🚀 Personal Executive Council")
        
        # Persona Selector - The "Command Center"
        with solara.Row(justify="center", style={"margin-bottom": "20px"}):
            solara.ToggleButtonsSingle(value=selected_persona, 
                                       values=["Career Expert", "Communication Coach"])
        
        with solara.Card(style={"background-color": "#f0f4f8"}):
            solara.Markdown(f"**Current Consultant:** {selected_persona.value}")
            solara.Markdown(f"*Focusing on your {target_degree.value} track.*")

        # Chat History
        for msg in chat_history.value:
            with solara.Card(style={"margin": "10px 0px"}):
                solara.Markdown(f"**{msg['role']}:** {msg['content']}")

        # Input
        solara.InputText(f"Ask the {selected_persona.value}...", 
                         value=user_prompt, on_value=user_prompt.set)
        
        def handle_click():
            result = run_persona_agent(user_prompt.value, selected_persona.value, target_degree.value)
            chat_history.set(chat_history.value + [
                {"role": "Me", "content": user_prompt.value},
                {"role": selected_persona.value, "content": result}
            ])
            user_prompt.set("")

        solara.Button(f"Consult {selected_persona.value}", on_click=handle_click, color="primary")

app = Page()