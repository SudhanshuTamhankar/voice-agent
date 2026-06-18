import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_stage4_flow():
    session_id = "test_user_target"
    
    # 1. Clear session
    client.delete(f"/session/{session_id}")

    # 2. Complete Profile immediately
    print("\n--- TURN 1: Provide full profile ---")
    query1 = "Hi, my 10th is 95, 12th is 89, engineering CGPA is 8.1. I'm a general male with 24 months work ex. I want to target IIM Ahmedabad, what percentile do I need?"
    print(f"User: {query1}")
    res1 = client.post("/ask", json={"query": query1, "session_id": session_id})
    data1 = res1.json()
    print(f"Intent Recognized: {data1.get('intent')}")
    print(f"Assistant:\n{data1.get('answer')}")

    time.sleep(2)

    # 3. Target FMS
    print("\n--- TURN 2: Target FMS Delhi ---")
    query2 = "What about FMS Delhi? What percentile should I target?"
    print(f"User: {query2}")
    res2 = client.post("/ask", json={"query": query2, "session_id": session_id})
    data2 = res2.json()
    print(f"Intent Recognized: {data2.get('intent')}")
    print(f"Assistant:\n{data2.get('answer')}")

    time.sleep(2)

    # 4. Target XLRI
    print("\n--- TURN 3: Target XLRI ---")
    query3 = "What score do I need for XLRI Jamshedpur?"
    print(f"User: {query3}")
    res3 = client.post("/ask", json={"query": query3, "session_id": session_id})
    data3 = res3.json()
    print(f"Intent Recognized: {data3.get('intent')}")
    print(f"Assistant:\n{data3.get('answer')}")

if __name__ == "__main__":
    test_stage4_flow()
