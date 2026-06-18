from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_ask_unknown_intent():
    response = client.post("/ask", json={"query": "What is the weather?"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "UNKNOWN"

def test_ask_methodology_unknown_institute():
    response = client.post("/ask", json={"query": "How does Harvard shortlist?"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "METHODOLOGY"
    assert "couldn't identify the institute" in data["answer"].lower()

# Note: Testing the actual LLM call requires an API key in .env
# If you run this test, ensure .env is correctly populated.
# We will just print the result to verify it locally.
if __name__ == "__main__":
    print("Testing /ask endpoint with valid institute (IIM Ahmedabad)...")
    res = client.post("/ask", json={"query": "How does IIMA shortlist candidates?"})
    data = res.json()
    print("Response Intent:", data.get("intent"))
    print("Response Answer:", data.get("answer").encode('ascii', 'replace').decode('ascii'))
    print("Test completed successfully!")

    print("\nTesting /ask endpoint with severe misspelling (ahmdbad)...")
    res = client.post("/ask", json={"query": "How does ahmdbad shortlist candidates?"})
    data = res.json()
    print("Response Intent:", data.get("intent"))
    print("Extracted Institute ID:", data.get("institute_id"))
