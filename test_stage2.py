import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_stage2_flow():
    session_id = "test_user_999"
    
    # 1. Clear session just in case
    client.delete(f"/session/{session_id}")

    # 2. Turn 1: Partial profile
    print("\n--- TURN 1 ---")
    query1 = "Hi, evaluate my profile. I'm a General Category male with 18 months work experience."
    print(f"User: {query1}")
    res1 = client.post("/ask", json={"query": query1, "session_id": session_id})
    data1 = res1.json()
    print(f"Assistant: {data1.get('answer')}")
    print(f"Profile Complete? {data1.get('profile_complete')}")

    print("Sleeping to respect rate limits...")
    time.sleep(4)

    # 3. Turn 2: Providing academics
    print("\n--- TURN 2 ---")
    query2 = "My 10th score is 95, 12th is 89, and I have an 8.1 CGPA in engineering."
    print(f"User: {query2}")
    res2 = client.post("/ask", json={"query": query2, "session_id": session_id})
    data2 = res2.json()
    print(f"Assistant: {data2.get('answer')}")
    print(f"Profile Complete? {data2.get('profile_complete')}")
    
    assert data2.get('profile_complete') == True, "Profile should be complete now!"
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_stage2_flow()
