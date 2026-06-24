import requests
import json
import time

URL = "http://localhost:8000/ask"

test_cases = [
    # ------------------ METHODOLOGY ------------------
    {
        "category": "Methodology", 
        "description": "FMS Delhi shortlisting to specifics (4 turns)", 
        "queries": [
            "how does FMS Delhi shortlist candidates for interview",
            "do they have a diversity bonus?",
            "what is their final selection criteria?",
            "how does Harvard Business School shortlist candidates?"
        ]
    },
    {
        "category": "Methodology", 
        "description": "IIM Ahmedabad details (4 turns)", 
        "queries": [
            "what is the selection criteria for IIM Ahmedabad",
            "how do they calculate the academic rating?",
            "do they consider work experience?",
            "does IIM Lucknow have a diversity bonus?"
        ]
    },

    # ------------------ PROFILE EVALUATION ------------------
    {
        "category": "Profile Evaluation", 
        "description": "Gradual profile building for IIM Indore (5 turns)", 
        "queries": [
            "can you evaluate my chances for IIM Indore?",
            "I got 85 percent in 10th class.",
            "and 88 percent in 12th class, and I am an engineer.",
            "I got 82 in graduation and have 24 months of work experience.",
            "I am a general male and my cat percentile is 98."
        ]
    },
    {
        "category": "Profile Evaluation", 
        "description": "Missing specific details for IIM Kozhikode (4 turns)", 
        "queries": [
            "Evaluate my chances for IIM Kozhikode.",
            "I have 12 months work experience and 99 percentile.",
            "I am a female with 90 in 10th, 92 in 12th, and 85 in grad.",
            "I am a general non-engineer."
        ]
    },

    # ------------------ TARGET PERCENTILE ------------------
    {
        "category": "Target Percentile", 
        "description": "Asking for target without profile (4 turns)", 
        "queries": [
            "what percentile do I need for IIM Calcutta?",
            "I am a general female with 90 in 10th and 95 in 12th.",
            "I got 85 in graduation and I am an engineer.",
            "I have 12 months of work experience."
        ]
    },
    {
        "category": "Target Percentile", 
        "description": "Impossible target profile followups (3 turns)", 
        "queries": [
            "what percentile do I need for IIM Bangalore? I have 60 in 10th.",
            "I also have 60 in 12th, 60 in grad, and 0 work ex.",
            "I am a general male engineer."
        ]
    },

    # ------------------ COLLEGE RECOMMENDATION ------------------
    {
        "category": "College Recommendation", 
        "description": "Asking for recommendations blankly (5 turns)", 
        "queries": [
            "which colleges should I apply to?",
            "I am an engineer.",
            "I have an 888 profile.",
            "I have 12 months of work experience and I am an NC-OBC male.",
            "my cat score is 92 percentile."
        ]
    },
    {
        "category": "College Recommendation", 
        "description": "Asking for colleges, then methodology (4 turns)", 
        "queries": [
            "Recommend colleges for me.",
            "EWS female, arts, 9/9/9, 12 months work ex, 98 percentile.",
            "Why did you recommend IIM Lucknow?",
            "what weight does IIM Bangalore give to work experience?"
        ]
    },

    # ------------------ OUT OF DOMAIN & EDGE CASES ------------------
    {
        "category": "Out of Domain -> Valid", 
        "description": "General Trivia to Evaluation (4 turns)", 
        "queries": [
            "what is the capital of France?",
            "okay fine. can you give me a study plan for DILR?",
            "I want to apply to IIM Calcutta.",
            "General male engineer, 90/90/90, 24 months work ex, 99.5 percentile."
        ]
    },
    {
        "category": "Edge Case", 
        "description": "Garbage input to invalid number recovery (4 turns)", 
        "queries": [
            "asdfghjkl",
            "Evaluate my profile for IIM Calcutta. I scored 105 percent in 12th.",
            "Oops, I meant 95 percent in 12th.",
            "General male engineer, 90 in 10th, 85 in grad, 12 months work ex, 99 percentile."
        ]
    }
]

def run_tests():
    report_lines = []
    report_lines.append("# Voice CLI Multi-Turn Stress Test Report (10 Deep Scenarios, 41 Queries)")
    report_lines.append("This report evaluates the agent's memory and conversational flow across 10 multi-turn scenarios (41 total queries).\n")
    
    with open("cli_multi_turn_stress_test_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")
    
    total_queries = sum(len(t['queries']) for t in test_cases)
    print(f"Starting {total_queries} queries across {len(test_cases)} scenarios...", flush=True)
    
    for i, test in enumerate(test_cases):
        scenario_lines = []
        session_id = f"stress_test_session_{i}_{int(time.time())}"
        scenario_lines.append(f"## Test Case {i+1}: {test['category']}")
        scenario_lines.append(f"**Description:** {test['description']}\n")
        
        for q in test['queries']:
            scenario_lines.append(f"> **User Speech:** '{q}'")
            print(f"[{i+1}/{len(test_cases)}] Sending: {q}", flush=True)
            
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    resp = requests.post(URL, json={"query": q, "session_id": session_id})
                    if resp.status_code == 500:
                        print(f"Rate limited (500). Retrying {attempt+1}/{max_retries} in 15 seconds...", flush=True)
                        time.sleep(15)
                        continue
                        
                    data = resp.json()
                    intent = data.get("intent", "UNKNOWN")
                    if "detail" in data:
                        answer = data["detail"]
                        intent = "ERROR"
                    else:
                        answer = data.get("answer", "")
                    
                    scenario_lines.append(f"> **🤖 Assistant [Intent: {intent}]:**\n> {answer}\n")
                    time.sleep(7) # GitHub 10 RPM limit safe buffer
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        scenario_lines.append(f"> **❌ Error:** {str(e)}\n")
                    time.sleep(7)
                
        scenario_lines.append("---\n")
        
        with open("cli_multi_turn_stress_test_report.md", "a", encoding="utf-8") as f:
            f.write("\n".join(scenario_lines) + "\n")
            
        print(f"Completed Test Case {i+1}: {test['category']}", flush=True)

    print("Test complete. Saved to cli_multi_turn_stress_test_report.md", flush=True)

if __name__ == "__main__":
    run_tests()
