from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_test():
    print("=== TEST 1: Semantic Parser (BLACKI) ===")
    response = client.post("/ask", json={
        "query": "What percentile should I target for blacki?",
        "session_id": "test_session_1"
    })
    print("Status:", response.status_code)
    print("Response:")
    print(response.json())

    print("\n=== TEST 2: Multiple Institutes ===")
    response = client.post("/ask", json={
        "query": "Evaluate my profile for IIM Ahmedabad and IIM Bangalore",
        "session_id": "test_session_2"
    })
    print("Status:", response.status_code)
    print("Response:")
    print(response.json())

    print("\n=== TEST 3: Provide Profile without Graduation Stream ===")
    response = client.post("/ask", json={
        "query": "I am an NC-OBC Male, 90 in 10th, 85 in 12th, 8 CGPA in grad, 97 percentile, 12 months work ex. Can you evaluate my profile for IIM Calcutta?",
        "session_id": "test_session_3"
    })
    print("Status:", response.status_code)
    print("Response:")
    data = response.json()
    # It should say profile_complete is True, because graduation_stream is no longer required!
    print("Profile Complete:", data.get("profile_complete"))
    # print answer, trim it down if it's too long
    print("Answer Preview:", data.get("answer")[:200] + "..." if data.get("answer") else None)

if __name__ == "__main__":
    run_test()
