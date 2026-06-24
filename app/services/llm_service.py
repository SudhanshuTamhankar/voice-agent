import json
import time
from openai import OpenAI, RateLimitError
from app.core.config import GITHUB_PAT, GROQ_API_KEY

class LLMService:
    """
    Wrapper around OpenAI SDK for Groq Cloud API.
    """
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set in the environment.")
        
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=GROQ_API_KEY
        )
        self.model_name = model_name

    def _execute_with_retry(self, func, *args, **kwargs):
        max_retries = 3
        base_delay = 2
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except RateLimitError as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(base_delay * (2 ** attempt))

    def generate_text(self, prompt: str) -> str:
        """
        Calls the model and returns the response text.
        """
        response = self._execute_with_retry(
            self.client.chat.completions.create,
            model=self.model_name,
            messages=[{"role": "system", "content": prompt}],
        )
        return response.choices[0].message.content

    def generate_json(self, prompt: str, response_schema=None) -> str:
        """
        Calls the model and enforces a JSON response format.
        Returns the raw JSON string.
        """
        # Append schema requirements to prompt since Structured Outputs might not be supported on all GitHub Models
        full_prompt = prompt
        if response_schema:
            full_prompt += f"\n\nYou MUST return your answer in valid JSON matching this schema: {json.dumps(response_schema)}"
        else:
            full_prompt += "\n\nYou MUST return your answer in valid JSON format."

        response = self._execute_with_retry(
            self.client.chat.completions.create,
            model=self.model_name,
            messages=[{"role": "system", "content": full_prompt}],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content

