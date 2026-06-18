import asyncio
import time
import sys
from app.main import app
from fastapi.testclient import TestClient

sys.stdout.reconfigure(encoding='utf-8')
client = TestClient(app)

def run_test():
    session_id = "test_stage3_session"
    
    # 1. Clear session
    client.delete(f"/session/{session_id}")
    
    print("--- TURN 1 (Incomplete Profile) ---")
    response1 = client.post("/ask", json={
        "query": "Is my profile good for IIM Ahmedabad? I have 95 in 10th and 18 months of work ex.",
        "session_id": session_id
    })
    print(f"User: Is my profile good for IIM Ahmedabad? I have 95 in 10th and 18 months of work ex.")
    print(f"Assistant: {response1.json()['answer']}")
    print(f"Profile Complete? {response1.json()['profile_complete']}")
    print("Sleeping to respect rate limits...\n")
    time.sleep(5)
    
    print("--- TURN 2 (Completing Profile) ---")
    response2 = client.post("/ask", json={
        "query": "I got 89 in 12th, 8.1 CGPA in Engineering, and I am a General Category Male.",
        "session_id": session_id
    })
    print(f"User: I got 89 in 12th, 8.1 CGPA in Engineering, and I am a General Category Male.")
    print(f"Assistant: {response2.json()['answer']}")
    print(f"Profile Complete? {response2.json()['profile_complete']}")
    
    print("--- TURN 3 (Evaluation) ---")
    response3 = client.post("/ask", json={
        "query": "Evaluate my profile for IIM Ahmedabad.",
        "session_id": session_id
    })
    print(f"User: Evaluate my profile for IIM Ahmedabad.")
    print(f"Assistant: {response3.json()['answer']}")
    print(f"Profile Complete? {response3.json()['profile_complete']}")

    if response2.status_code != 200 or response3.status_code != 200:
        print("Error in API")
    
if __name__ == "__main__":
    run_test()
