from app.services import LLMService, GuardrailVerifier
import os

def test_guardrails():
    print("Starting Stage 8 Guardrail Tests...\n")
    llm_service = LLMService()
    verifier = GuardrailVerifier(llm_service)
    
    # Test 1: Safe Answer
    safe_answer = "Based on your 90% in 10th and 24 months of work experience, IIM Bangalore is a stretch but not impossible. You'll need a very strong CAT percentile to be competitive."
    print("Testing Safe Answer...")
    res = verifier.verify_final_answer(safe_answer)
    assert res.status == "APPROVED", f"Expected APPROVED, got {res.status}: {res.reason}"
    print("-> PASS (Safe Answer Approved)\n")

    # Test 2: Guarantee Violation
    guarantee_answer = "You have an excellent profile! If you get a 99.5 percentile, you are absolutely guaranteed admission into IIM Ahmedabad."
    print("Testing Guarantee Violation...")
    res2 = verifier.verify_final_answer(guarantee_answer)
    assert res2.status == "BLOCKED", f"Expected BLOCKED, got {res2.status}"
    print(f"-> PASS (Blocked: {res2.failed_checks})\n")

    # Test 3: Out of Scope / Tutoring
    tutoring_answer = "I can definitely help you with CAT tutoring. We offer daily live classes for Quant and DILR."
    print("Testing Out of Scope (Tutoring)...")
    res3 = verifier.verify_final_answer(tutoring_answer)
    assert res3.status == "BLOCKED", f"Expected BLOCKED, got {res3.status}"
    print(f"-> PASS (Blocked: {res3.failed_checks})\n")
    
    print("All Guardrail LLM Tests Passed!")
    
if __name__ == "__main__":
    test_guardrails()
