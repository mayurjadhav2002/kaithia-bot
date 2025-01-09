import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

prompts = []

generation_config = {
    "temperature": 0.95,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

extra_prompts=

class BotOperation:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )
        self.user = None

    def append_prompt(self, text, type="input"):
        prompts.append(f"{type}: {text}")

    def Generative(self, message):
        self.append_prompt(message, "input")
        response = self.model.generate_content(prompts)
        
        if hasattr(response, "text"):
            response_text = response.text
            self.append_prompt(response_text, "output")
            return response_text
        else:
            print("Error: 'GenerateContentResponse' object has no attribute 'text'")
            return None

  