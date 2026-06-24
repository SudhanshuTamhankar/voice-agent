import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.services.audio_service import SpeechToTextService, TextToSpeechService
from app.services.telemetry import TelemetryService

def run_voice_chat():
    client = TestClient(app)
    session_id = str(uuid.uuid4())
    
    stt = SpeechToTextService()
    tts = TextToSpeechService()
    telemetry = TelemetryService()
    
    telemetry.track_event("voice.session_started", session_id)
    
    print("="*60)
    print("🎙️ Welcome to the AI Voice Admissions Assistant (Voice Mode)")
    print("Speak clearly into your microphone.")
    print("Press Ctrl+C to stop.")
    print("="*60)
    print()

    # Initial greeting
    tts.speak("Welcome to the AI Admissions Assistant. How can I help you today?")

    while True:
        try:
            # 1. Listen to the user
            user_input = stt.listen_and_transcribe()
            
            if not user_input.strip():
                continue
                
            if user_input.lower() in ['exit', 'quit', 'stop']:
                tts.speak("Goodbye! Best of luck with your CAT prep!")
                print("Goodbye!")
                break
                
            # 2. Call the Assistant Engine (using TestClient to bypass network stack)
            try:
                response = client.post("/ask", json={"query": user_input, "session_id": session_id})
                data = response.json()
                
                intent = data.get("intent", "UNKNOWN")
                answer = data.get("answer", "I didn't quite get that.")
                
                print(f"\n🤖 Assistant [Intent: {intent}]:\n{answer}")
                
                # 3. Speak the answer
                tts.speak(answer)
                
            except Exception as e:
                print(f"\n[Error connecting to logic: {e}]")
                tts.speak("Sorry, I encountered an error connecting to my logic engine.")
                
        except KeyboardInterrupt:
            print("\nStopping voice session...")
            break

if __name__ == "__main__":
    run_voice_chat()
