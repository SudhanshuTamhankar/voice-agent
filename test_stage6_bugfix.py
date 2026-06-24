from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_bugfix_test():
    print("Starting Bugfix Test...")
    
    session_id = "test_bugfix_session_1"
    
    # Test 1: Out of Domain
    print("\n--- Test 1: Out of Domain ---")
    query1 = "What is the capital of India?"
    response1 = client.post("/ask", json={"query": query1, "session_id": session_id}).json()
    
    assert response1["intent"] == "OUT_OF_DOMAIN", f"Got intent {response1.get('intent')}"
    print("Test 1 OK! (Caught out of domain)")
    
    # Test 2: Validation Error (Cat Percentile > 100)
    print("\n--- Test 2: Validation Bounds ---")
    query2 = "I have 101.98 percentile in CAT"
    response2 = client.post("/ask", json={"query": query2, "session_id": session_id}).json()
    print("Response 2:", response2)
    assert "bounds" in response2["answer"].lower() or "100" in response2["answer"].lower()
    print("Test 2 OK! (Caught bounds error)")
    
    print("\nAll bugfix tests passed!")

if __name__ == "__main__":
    run_bugfix_test()
