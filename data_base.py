import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
for m in genai.list_models():
    if "embed" in m.name.lower():
        print(m.name, m.supported_generation_methods)