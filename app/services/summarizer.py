import google.generativeai as genai
import os

def summarize_with_gemini(text: str) -> str:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    prompt = f"Summarize the following text:\n{text}"
    response = model.generate_content([prompt])
    return response.text.strip()
