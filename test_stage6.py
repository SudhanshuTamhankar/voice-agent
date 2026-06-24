from fastapi.testclient import TestClient
from app.main import app
import time

client = TestClient(app)

def run_multi_turn_test():
    print("Starting Multi-Turn Context Memory Test (Stage 6)...")
    
    session_id = "test_stage6_session_1"
    
    # Turn 1: Provide full profile and ask for IIMA
    print("\n--- Turn 1: Full Profile for IIMA ---")
    query1 = "Can you evaluate my profile for IIM Ahmedabad? I am a general male with 90 in 10th, 90 in 12th, 80% in graduation (engineering), 0 work experience, and my CAT percentile is 99.8"
    response1 = client.post("/ask", json={"query": query1, "session_id": session_id}).json()
    
    assert response1["intent"] == "PROFILE_EVALUATION"
    assert response1["institute_id"] == "iim_ahmedabad", f"Got {response1.get('institute_id')}"
    assert response1["profile_complete"] == True
    print("Turn 1 OK!")
    
    time.sleep(4) # Prevent rate-limiting
    
    # Turn 2: Follow-up without profile -> Switch to IIM Bangalore
    print("\n--- Turn 2: What about Bangalore? ---")
    query2 = "And what about IIM Bangalore?"
    response2 = client.post("/ask", json={"query": query2, "session_id": session_id}).json()
    
    assert response2["intent"] == "PROFILE_EVALUATION"
    assert response2["institute_id"] == "iim_bangalore", f"Got {response2.get('institute_id')}"
    assert response2["profile_complete"] == True
    print("Turn 2 OK!")
    
    time.sleep(4)
    
    # Turn 3: Contextual Intent Switch (TARGET_PERCENTILE without specifying institute)
    print("\n--- Turn 3: What percentile do I need? ---")
    query3 = "What percentile do I need to convert it?"
    response3 = client.post("/ask", json={"query": query3, "session_id": session_id}).json()
    
    # Because of context carry-forward, it should stick to IIM Bangalore
    assert response3["intent"] == "TARGET_PERCENTILE"
    assert response3["institute_id"] == "iim_bangalore", f"Got {response3.get('institute_id')}"
    print("Turn 3 OK!")
    
    time.sleep(4)
    
    # Turn 4: Profile Delta Update
    print("\n--- Turn 4: Profile update ---")
    query4 = "What if I get 24 months of work experience?"
    response4 = client.post("/ask", json={"query": query4, "session_id": session_id}).json()
    
    # Usually maps to PROFILE_EVALUATION
    assert response4["intent"] in ["PROFILE_EVALUATION", "TARGET_PERCENTILE", "UNKNOWN"]
    assert response4["institute_id"] == "iim_bangalore", f"Got {response4.get('institute_id')}"
    print("Turn 4 OK!")

    time.sleep(4)

    # Turn 5: Contextual Methodology intent
    print("\n--- Turn 5: Methodology Question ---")
    query5 = "How much weightage do they give to academics?"
    response5 = client.post("/ask", json={"query": query5, "session_id": session_id}).json()

    assert "intent" in response5, f"Missing 'intent'. Got: {response5}"
    assert response5["intent"] == "METHODOLOGY"
    assert response5["institute_id"] == "iim_bangalore", f"Got {response5.get('institute_id')}"
    print("Turn 5 OK!")
    
    print("\nAll Stage 6 context tests passed!")

if __name__ == "__main__":
    run_multi_turn_test()
