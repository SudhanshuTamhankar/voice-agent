import subprocess
import time
import re

models_to_try = [
    "gemini-2.5-flash",
    "gemini-2.0-flash-001",
    "gemini-2.0-flash-lite-001",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-pro-latest"
]

def update_model(model_name):
    path = r"app\services\llm_service.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_content = re.sub(r'def __init__\(self, model_name: str = ".*"\):', f'def __init__(self, model_name: str = "{model_name}"):', content)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    success = False
    for model in models_to_try:
        print(f"\n==============================================")
        print(f"Trying model: {model}")
        update_model(model)
        
        # Run the test script
        result = subprocess.run(["python", "test_stage2.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"SUCCESS! {model} passed the test.")
            print(result.stdout)
            success = True
            break
        else:
            print(f"FAILED! {model} failed.")
            error_lines = [line for line in result.stderr.split('\n') if line.strip()]
            print("Error tail:", "\n".join(error_lines[-5:]))
        
        # Sleep to avoid immediate rate limits on the next call
        print("Sleeping 5 seconds before next model...")
        time.sleep(5)
    
    if not success:
        print("All models failed.")
