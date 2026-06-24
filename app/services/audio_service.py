import os
import asyncio
import speech_recognition as sr
import edge_tts
import pygame

class SpeechToTextService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Increase the pause threshold to allow users to take a breath or think mid-sentence
        # The default is 0.8 seconds. 3.0 seconds gives a much more forgiving listening experience.
        self.recognizer.pause_threshold = 3.0
        
    def listen_and_transcribe(self) -> str:
        """
        Listens to the microphone and transcribes the audio to text using Google's free Web Speech API.
        Blocks until speech is recognized or an error occurs.
        """
        with sr.Microphone() as source:
            print("\n[ASR] Adjusting for ambient noise... Please wait.")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("[ASR] Listening... (Speak now)")
            try:
                # Listen for user's speech
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=30)
                print("[ASR] Processing audio...")
                
                # Transcribe using Google Web Speech API
                text = self.recognizer.recognize_google(audio, language="en-IN")
                print(f"[ASR] Transcript: '{text}'")
                return text
                
            except sr.WaitTimeoutError:
                print("[ASR] Error: Listening timed out. No speech detected.")
                return ""
            except sr.UnknownValueError:
                print("[ASR] Error: Could not understand audio.")
                return ""
            except sr.RequestError as e:
                print(f"[ASR] Error: Could not request results from Google Speech Recognition service; {e}")
                return ""

class TextToSpeechService:
    def __init__(self, voice="en-IN-NeerjaExpressiveNeural"):
        """
        Initializes the TTS Service.
        Default voice: 'en-IN-NeerjaExpressiveNeural' (Indian English Female).
        Other good voices: 'en-IN-PrabhatExpressiveNeural' (Indian English Male).
        """
        self.voice = voice
        pygame.mixer.init()
        
    async def _generate_and_play(self, text: str):
        output_file = "response_audio.mp3"
        
        # Strip markdown characters that sound bad in TTS
        import re
        # Remove bold/italic asterisks and underscores
        clean_text = re.sub(r'[*_]{1,3}', '', text)
        # Remove markdown headers (#)
        clean_text = re.sub(r'#+\s*', '', clean_text)
        # Remove markdown links [text](url) -> text
        clean_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_text)
        
        # Generate audio file
        communicate = edge_tts.Communicate(clean_text, self.voice)
        await communicate.save(output_file)
        
        # Play audio using pygame
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        
        # Block until audio finishes playing
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
            
        # Unload and clean up the file
        pygame.mixer.music.unload()
        try:
            os.remove(output_file)
        except OSError:
            pass

    def speak(self, text: str):
        """
        Converts text to speech and plays it through the speakers synchronously.
        """
        print(f"\n[TTS] Generating speech...")
        asyncio.run(self._generate_and_play(text))
