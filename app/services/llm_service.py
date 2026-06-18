from google import genai
from app.core.config import GEMINI_API_KEY

class LLMService:
    """
    Wrapper around google-genai SDK for Gemini models.
    """
    def __init__(self, model_name: str = "gemini-flash-lite-latest"):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in the environment.")
        
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = model_name

    def generate_text(self, prompt: str) -> str:
        """
        Calls the Gemini model and returns the response text.
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        return response.text

    def generate_json(self, prompt: str, response_schema=None) -> str:
        """
        Calls the Gemini model and enforces a JSON response format.
        Returns the raw JSON string.
        """
        config = {"response_mime_type": "application/json"}
        if response_schema:
            config["response_schema"] = response_schema
            
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=config
        )
        return response.text
