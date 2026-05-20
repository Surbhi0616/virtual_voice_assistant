import sys
import pyttsx3
from llm_generation import generate_voice_response
from stt_listener import listen_to_microphone

def speak_text(text):
    print("🔊 Speaking response...")
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)    
    engine.setProperty('volume', 1.0)  
    
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id) 
        
    engine.say(text)
    engine.runAndWait()

def run_voice_assistant_app():
    print("==================================================")
    print("   🎙️ FULLY HANDS-FREE VOICE CLAIMS ASSISTANT   ")
    print("==================================================")
    print("Press Ctrl+C at any time in the terminal to exit.\n")
    
    while True:
        print("\nReady for your next question...")
        input("👉 Press [ENTER] when you are ready to speak...")
        
        # 1. Capture voice from microphone instead of typing input
        user_query = listen_to_microphone()
        
        if not user_query:
            print("Let's try again. Please speak clearly into your mic.")
            continue
            
        if user_query.lower() in ['exit', 'quit', 'stop']:
            print("Closing the assistant. Have a wonderful day!")
            break
            
        print("\n🤖 Processing your voice request...")
        try:
            # 2. Feed the spoken transcript straight into your RAG pipeline
            ai_text_response = generate_voice_response(user_query)
            
            print(f"\n🏆 ANSWER: {ai_text_response}\n")
            
            # 3. Read it out loud
            speak_text(ai_text_response)
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nShutting down gracefully...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    try:
        run_voice_assistant_app()
    except KeyboardInterrupt:
        print("\nProgram closed. Goodbye!")
        sys.exit(0)