import uuid
from fastapi.testclient import TestClient
from app.main import app

def run_chat():
    client = TestClient(app)
    session_id = str(uuid.uuid4())
    
    print("="*60)
    print("🤖 Welcome to the AI Voice Admissions Assistant (CLI Test Mode)")
    print("Type 'exit' or 'quit' to stop.")
    print("Type 'clear' to reset your session profile.")
    print("="*60)
    print()

    while True:
        try:
            user_input = input("\nYou: ")
        except (KeyboardInterrupt, EOFError):
            break
            
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
            
        if user_input.lower() == 'clear':
            client.delete(f"/session/{session_id}")
            print("[System: Profile session cleared]")
            continue
            
        if not user_input.strip():
            continue

        try:
            response = client.post("/ask", json={"query": user_input, "session_id": session_id})
            data = response.json()
            
            intent = data.get("intent", "UNKNOWN")
            answer = data.get("answer", "No answer provided")
            
            print(f"\n🤖 Assistant [Intent: {intent}]:\n{answer}")
            
        except Exception as e:
            print(f"\n[Error connecting to logic: {e}]")

if __name__ == "__main__":
    run_chat()
