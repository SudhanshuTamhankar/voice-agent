import os
import time
import json
from fastapi.testclient import TestClient

# We need to import the FastAPI app. Let's assume it's in app.main
try:
    from app.main import app
except ImportError:
    print("Could not import app.main. Creating a temporary app with routes.")
    from fastapi import FastAPI
    import sys
    from dotenv import load_dotenv
    load_dotenv()
    from app.api.routes import router
    app = FastAPI()
    app.include_router(router)

client = TestClient(app)

# 30 Scenarios, ~100 queries total
scenarios = [
    {
        "name": "Scenario 1: Methodology IIM Ahmedabad",
        "queries": [
            "How does IIM Ahmedabad shortlist candidates for the interview?",
            "What is the weightage of the CAT score for IIM A?",
            "Do they consider 10th and 12th marks?"
        ]
    },
    {
        "name": "Scenario 2: Methodology IIM Bangalore",
        "queries": [
            "What is the selection criteria for IIM Bangalore?",
            "How much weightage does work experience hold at IIM B?",
            "Do they normalize graduation scores?"
        ]
    },
    {
        "name": "Scenario 3: Methodology IIM Calcutta",
        "queries": [
            "Explain IIM Calcutta's admission methodology.",
            "Is there any diversity points for female candidates at IIM C?",
            "How much CAT weightage is there for final selection?"
        ]
    },
    {
        "name": "Scenario 4: Methodology IIM Lucknow",
        "queries": [
            "How does IIM Lucknow calculate the composite score?",
            "What are the academic diversity marks?",
            "Are 12th marks considered for the PI shortlist?"
        ]
    },
    {
        "name": "Scenario 5: Methodology IIM Kozhikode",
        "queries": [
            "What is the criteria for IIM Kozhikode?",
            "Is there a gender diversity factor?",
            "Do they give marks for professional qualifications like CA/CS?"
        ]
    },
    {
        "name": "Scenario 6: Methodology IIM Indore",
        "queries": [
            "How does IIM Indore shortlist?",
            "Why is 10th and 12th weightage so high at IIM Indore?",
            "What is the weightage of the personal interview?"
        ]
    },
    {
        "name": "Scenario 7: Target Percentile GEM IIMA",
        "queries": [
            "What percentile should I target for IIM Ahmedabad?",
            "I am a GEM (General Engineer Male).",
            "My 10th is 95, 12th is 92, and graduation is 8.5 CGPA. I have 24 months of work experience."
        ]
    },
    {
        "name": "Scenario 8: Target Percentile GNEF IIMB",
        "queries": [
            "I want to know the target percentile for IIM Bangalore.",
            "My profile: General Non-Engineer Female, 10th 90%, 12th 92%, Grad 82%, Fresher."
        ]
    },
    {
        "name": "Scenario 9: Target Percentile SC Male IIMC",
        "queries": [
            "Target percentile for IIM Calcutta?",
            "I am an SC category Male.",
            "My academics are 80 in 10th, 75 in 12th, and 70 in graduation. I have 12 months work ex."
        ]
    },
    {
        "name": "Scenario 10: Target Percentile NC-OBC Female IIML",
        "queries": [
            "What is the required CAT percentile for IIM Lucknow?",
            "I am an NC-OBC Female, Engineer.",
            "10th: 88, 12th: 85, Grad: 8.0. Work ex is 36 months."
        ]
    },
    {
        "name": "Scenario 11: Target Percentile EWS Male IIMK",
        "queries": [
            "Target percentile for IIM Kozhikode for EWS Male?",
            "Acads: 9/9/8. Fresher."
        ]
    },
    {
        "name": "Scenario 12: Target Percentile FMS Delhi",
        "queries": [
            "What percentile do I need for FMS Delhi?",
            "I am a General category male, 9/9/9 profile, 2 years work experience."
        ]
    },
    {
        "name": "Scenario 13: College Rec GEM 99.5",
        "queries": [
            "Which colleges can I get into?",
            "I am a GEM with 99.5 percentile in CAT.",
            "My acads are 9/9/9 and I have 24 months work ex."
        ]
    },
    {
        "name": "Scenario 14: College Rec GNEF 98",
        "queries": [
            "Recommend me some good B-schools.",
            "I am a GNEF, 98 percentile, 8/8/8 acads, Fresher."
        ]
    },
    {
        "name": "Scenario 15: College Rec NC-OBC Male 95",
        "queries": [
            "What are my options with a 95 percentile?",
            "I belong to NC-OBC category, Male, Engineer.",
            "Academics: 75 in 10th, 78 in 12th, 7.5 CGPA in grad. Work experience: 12 months."
        ]
    },
    {
        "name": "Scenario 16: College Rec SC Female 90",
        "queries": [
            "Please recommend colleges for me.",
            "SC category, Female.",
            "90 percentile in CAT, 8/8/8 profile, fresher."
        ]
    },
    {
        "name": "Scenario 17: College Rec Partial Profile",
        "queries": [
            "Which IIMs can I get?",
            "I am a GEM with 9/9/9."
            # Missing CAT score
        ]
    },
    {
        "name": "Scenario 18: Profile Eval GEM IIMA",
        "queries": [
            "Evaluate my profile for IIM Ahmedabad.",
            "GEM, 9/9/9, 99.8 percentile, 36 months work ex."
        ]
    },
    {
        "name": "Scenario 19: Profile Eval GNEF IIMB",
        "queries": [
            "Is my profile good enough for IIM Bangalore?",
            "General Non-Engineer Female, 10th 85%, 12th 88%, Grad 80%.",
            "99 percentile in CAT, 0 work experience."
        ]
    },
    {
        "name": "Scenario 20: Profile Eval NC-OBC IIMC",
        "queries": [
            "Profile evaluation for IIM Calcutta.",
            "NC-OBC Male, 90 in 10th, 85 in 12th, 8 CGPA in grad, 97 percentile, 12 months work ex."
        ]
    },
    {
        "name": "Scenario 21: Profile Eval EWS IIML",
        "queries": [
            "Evaluate my chances for IIM Lucknow.",
            "EWS Female, 80/75/80 acads, 96 percentile, 24 months work ex."
        ]
    },
    {
        "name": "Scenario 22: Profile Eval SC IIMK",
        "queries": [
            "How are my chances for IIM Kozhikode?",
            "SC Male, 7/7/7 acads, 92 percentile, Fresher."
        ]
    },
    {
        "name": "Scenario 23: Profile Eval FMS Delhi",
        "queries": [
            "Evaluate my profile for FMS.",
            "GEM, 8/8/8, 99 percentile."
        ]
    },
    {
        "name": "Scenario 24: Multi-turn College Rec",
        "queries": [
            "I want college recommendations.",
            "I am a General Male.",
            "I am an engineer with 2 years of work ex.",
            "My acads are 85% in 10th, 90% in 12th and 8.2 in grad.",
            "My CAT percentile is 98.5."
        ]
    },
    {
        "name": "Scenario 25: Multi-turn Profile Eval",
        "queries": [
            "Can you evaluate my profile?",
            "For IIM Indore.",
            "I am an NC-OBC female, fresher.",
            "My acads are 9/9/9.",
            "I am expecting 96 percentile."
        ]
    },
    {
        "name": "Scenario 26: Methodology SPJIMR",
        "queries": [
            "What is the admission process for SPJIMR?",
            "Do they have profile based calls?",
            "What are the parameters for the profile based calls?"
        ]
    },
    {
        "name": "Scenario 27: Profile Eval BLACKI",
        "queries": [
            "Evaluate my profile for blacki.",
            "GEM, 9/9/9, 99.5 percentile, 18 months work ex."
        ]
    },
    {
        "name": "Scenario 28: Target Percentile BLACKI",
        "queries": [
            "What percentile should I target for blacki?",
            "I am an ST category male, non-engineer, 8/8/8, fresher."
        ]
    },
    {
        "name": "Scenario 29: Methodology XLRI",
        "queries": [
            "How does XLRI select candidates?",
            "Does it accept CAT score?",
            "What is the weightage of XAT score?"
        ]
    },
    {
        "name": "Scenario 30: College Rec SPJIMR & XLRI",
        "queries": [
            "Can I get into SPJIMR or XLRI?",
            "I am a General Female, 90 in 10th, 92 in 12th, 8.5 CGPA.",
            "I have 97 percentile in CAT."
        ]
    }
]

def run_stress_test():
    report_file = "readme.md"
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# Gemini API Stress Test Report\n\n")
        
        for i, scenario in enumerate(scenarios):
            print(f"Running {scenario['name']}...")
            f.write(f"## {scenario['name']}\n\n")
            session_id = f"stress_test_session_{i}"
            
            # Clear session first just in case
            client.delete(f"/session/{session_id}")
            
            for query in scenario['queries']:
                f.write(f"**User**: {query}\n\n")
                f.flush()
                
                max_retries = 3
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        response = client.post(
                            "/ask",
                            json={"query": query, "session_id": session_id}
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            answer = data.get("answer", "No answer provided.")
                            f.write(f"**Agent**: {answer}\n\n")
                            break
                        elif response.status_code == 500 and "429" in response.text:
                            print("Rate limit hit, sleeping for 45 seconds...")
                            time.sleep(45)
                            retry_count += 1
                        else:
                            f.write(f"**Agent (Error {response.status_code})**: {response.text}\n\n")
                            break
                    except Exception as e:
                        f.write(f"**Agent (Exception)**: {str(e)}\n\n")
                        break
                        
                f.flush()
                time.sleep(3) # Safe sleep for Groq 30 RPM API limit
                
            f.write("---\n\n")

if __name__ == "__main__":
    run_stress_test()
    print("Stress test completed. Report generated in readme.md.")
