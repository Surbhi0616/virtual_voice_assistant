import speech_recognition as sr

def listen_to_microphone():
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    # Adjust sensitivity for background ambient noise
    recognizer.dynamic_energy_threshold = True
    
    with sr.Microphone() as source:
        print("\n🎤 Listening... Speak your question now.")
        # Calibrate for 1 second to handle background hiss
        recognizer.adjust_for_ambient_noise(source, duration=1.0)
        
        try:
            # Listen for the user's voice input
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("⏳ Transcribing audio...")
            
            # Convert speech to text using Google's free web recognizer
            text_query = recognizer.recognize_google(audio_data)
            print(f"🗣️ You said: \"{text_query}\"")
            return text_query
            
        except sr.WaitTimeoutError:
            print("❌ Silence detected. No one spoke.")
            return None
        except sr.UnknownValueError:
            print("❌ Sorry, I couldn't understand the audio clearly.")
            return None
        except sr.RequestError as e:
            print(f"❌ Could not request results from speech service; {e}")
            return None

if __name__ == "__main__":
    # Test the microphone directly
    print("--- Testing Microphone Function ---")
    listen_to_microphone()