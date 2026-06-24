import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_tests():
    print("Starting Automated Stress Test (Sampling 1 prompt per category)...\n")
    
    test_cases = [
        # 1. Profile Accumulation Edge Cases
        {
            "category": "1. Messy Profile Dump",
            "query": "I am an OBC non-creamy layer female from an arts background. I scored 8.2 CGPA in 10th, 84 percent in 12th, and my graduation score is 71 percent. I have been working for 42 months and I expect a 98 percentile in CAT. Evaluate me for IIM Calcutta.",
            "session_id": "stress_test_1"
        },
        # 2. Mathematically Impossible
        {
            "category": "2. Impossible Gap",
            "query": "I am a general male engineer. 60% in 10th, 65% in 12th, 60% in graduation. 0 work experience. What CAT percentile do I need for IIM Bangalore?",
            "session_id": "stress_test_2"
        },
        # 3. Contextual Memory & Intent Switching
        {
            "category": "3. Contextual Memory (Turn 1)",
            "query": "How does FMS Delhi shortlist candidates?",
            "session_id": "stress_test_3"
        },
        {
            "category": "3. Contextual Memory (Turn 2)",
            "query": "Okay, but what percentile do I need to get a call from there?",
            "session_id": "stress_test_3"
        },
        # 4. Guardrail & Information Leakage Tests
        {
            "category": "4. Guardrail / Guarantee Trap",
            "query": "If I score exactly what you said, 99.5 percentile, do you guarantee I will get a call?",
            "session_id": "stress_test_4"
        },
        # 5. Out-of-Domain & Competitor Redirects
        {
            "category": "5. Out of Domain (Clymber Redirect)",
            "query": "Can you generate a 30-day study plan for DILR?",
            "session_id": "stress_test_5"
        },
        # 7. College Recommendation Gating
        {
            "category": "7. College Recommendation Gating",
            "query": "I have a 9/9/9 profile, general male, 24 months work ex. Which colleges should I apply to?",
            "session_id": "stress_test_7"
        }
    ]

    for tc in test_cases:
        print(f"--- Running Category: {tc['category']} ---")
        print(f"User: '{tc['query']}'")
        
        try:
            response = client.post("/ask", json={"query": tc["query"], "session_id": tc["session_id"]}).json()
            
            if "detail" in response:
                print(f"ERROR: {response['detail']}\n")
            else:
                print(f"Intent Classified: {response.get('intent')}")
                print(f"Institute Identified: {response.get('institute_id')}")
                print(f"Assistant Answer:\n{response.get('answer')}\n")
        except Exception as e:
            print(f"CRITICAL EXCEPTION: {e}\n")
            
        # VERY slow pacing to avoid 429 RESOURCE_EXHAUSTED (15 req/min limit = 4s/req. Each turn does ~4 LLM calls = 16 seconds needed per turn)
        print("Sleeping 18s to avoid LLM rate limits...\n")
        time.sleep(18)

if __name__ == "__main__":
    run_tests()
