from app.schemas.profile import UserProfile
from app.services.profile_validator import ProfileValidator
from app.main import app
from fastapi.testclient import TestClient

def run_tests():
    print("Testing profile validation...")
    profile = UserProfile(
        category="GENERAL",
        gender="MALE",
        class_10_score=90,
        class_12_score=90,
        graduation_score=80,
        graduation_stream="ENGINEERING",
        work_ex_months=0
    )
    
    missing = ProfileValidator.get_missing_fields(profile)
    assert "actual_percentile" not in missing, "actual_percentile should NOT be required by default"
    
    missing = ProfileValidator.get_missing_fields(profile, require_exam_score=True)
    assert "actual_percentile" in missing, "actual_percentile SHOULD be required for evaluation"
    print("Validation ok!")

    print("Testing memory context...")
    client = TestClient(app)
    session_id = "test_memory_session_123"
    
    response1 = client.post("/ask", json={"query": "hi can you please analyse my profile for iim b ?", "session_id": session_id})
    data1 = response1.json()
    assert data1["intent"] == "PROFILE_EVALUATION"
    assert data1["profile_complete"] == False
    
    response2 = client.post("/ask", json={
        "query": "i a general male with 92.3 in 10th, 90 in 12th 7.3 cg in graduation with engineering and zero experience and my cat percentile is 99.67",
        "session_id": session_id
    })
    data2 = response2.json()
    print(f"DEBUG data2: {data2}")
    assert data2["institute_id"] == "IIM Bangalore", f"Expected IIM Bangalore, got {data2.get('institute_id')}"
    assert data2["profile_complete"] == True
    print("Memory ok!")
    print("All tests passed.")

if __name__ == "__main__":
    run_tests()
