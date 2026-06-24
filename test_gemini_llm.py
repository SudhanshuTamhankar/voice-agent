import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def test_gemini():
    if not GEMINI_API_KEY:
        print("No GEMINI_API_KEY found.")
        return
        
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents="Hello! Are you working?",
        )
        print("Success!")
        print(response.text)
    except Exception as e:
        print("Error:")
        print(e)

if __name__ == "__main__":
    test_gemini()
