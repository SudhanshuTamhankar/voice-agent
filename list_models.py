import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def list_models():
    if "GEMINI_API_KEY" not in os.environ:
        print("GEMINI_API_KEY is not set.")
        return
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    
    print("Available models:")
    for model in client.models.list():
        print(f"- {model.name}")

if __name__ == "__main__":
    list_models()
