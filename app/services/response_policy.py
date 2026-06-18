class ResponsePolicy:
    """
    Applies guardrails to the LLM response.
    Ensures that low-confidence data isn't hallucinated or presented as absolute truth.
    """
    
    @staticmethod
    def apply_guardrails(response_text: str, confidence: str) -> str:
        # For Low confidence, ensure we add a disclaimer if the LLM forgot to.
        if confidence and confidence.lower() == "low":
            warning = (
                "\n\n*Note: Official explicit methodology weightings for this institute are currently unverified or unavailable. "
                "The above is based on broad historical/general guidelines.*"
            )
            if "unverified" not in response_text.lower() and "unavailable" not in response_text.lower():
                response_text += warning
                
        return response_text
