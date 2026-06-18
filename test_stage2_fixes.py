import pytest
from app.schemas.profile import UserProfile, ProfileDelta
from app.services.profile_validator import ProfileValidator
from app.api.routes import app
from fastapi.testclient import TestClient

def test_profile_validator_requires_exam_score():
    profile = UserProfile(
        category="GENERAL",
        gender="MALE",
        class_10_score=90,
        class_12_score=90,
        graduation_score=80,
        graduation_stream="ENGINEERING",
        work_ex_months=0
    )
    
    # Standard check should not require exam score
    missing = ProfileValidator.get_missing_fields(profile)
    assert "actual_percentile" not in missing
    
    # But evaluating profile should require it
    missing = ProfileValidator.get_missing_fields(profile, require_exam_score=True)
    assert "actual_percentile" in missing

def test_session_memory_target_institute():
    client = TestClient(app)
    session_id = "test_memory_session_123"
    
    # Turn 1: User asks for IIM B
    response1 = client.post("/ask", json={"query": "hi can you please analyse my profile for iim b ?", "session_id": session_id})
    assert response1.status_code == 200
    data1 = response1.json()
    assert data1["intent"] == "PROFILE_EVALUATION"
    # Should ask for profile fields
    assert data1["profile_complete"] == False
    
    # Turn 2: User provides profile, but doesn't mention IIM B again
    response2 = client.post("/ask", json={
        "query": "i a general male with 92.3 in 10th, 90 in 12th 7.3 cg in graduation with engineering and zero experience and my cat percentile is 99.67",
        "session_id": session_id
    })
    data2 = response2.json()
    
    # It should remember IIM Bangalore (which is the standardized institute_id)
    assert data2["institute_id"] == "IIM Bangalore"
    assert data2["profile_complete"] == True
