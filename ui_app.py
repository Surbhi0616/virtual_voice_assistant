import streamlit as st
from llm_generation import generate_voice_response
from stt_listener import listen_to_microphone
import pyttsx3
import threading

# --- Helper function to run TTS in a background thread ---
# This prevents the web browser from freezing while your computer speaks!
def speak_text_async(text):
    def tts_worker(text_to_speak):
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 175)
            voices = engine.getProperty('voices')
            if len(voices) > 1:
                engine.setProperty('voice', voices[1].id)
            engine.say(text_to_speak)
            engine.runAndWait()
        except Exception as e:
            pass

    threading.Thread(target=tts_worker, args=(text,), daemon=True).start()

# --- Streamlit Page Configurations ---
st.set_page_config(page_title="Voice Claims Assistant", page_icon="🎙️", layout="centered")

st.title("Voice enabled intelligent virtual Assistant")
st.markdown("Interact with your local vector database hands-free or via text query.")
st.write("---")

# Initialize chat session memory for the UI display
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ System Control Center")
    st.info("🤖 **LLM Brain:** `llama3.2:1b` \n\n📁 **Vector Store:** `nomic-embed-text`")
    
    st.write("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Top Interface: Voice Trigger Button ---
st.subheader("Speak to Assistant")
col1, col2 = st.columns([1, 4])

with col1:
    voice_clicked = st.button("🎤 Click & Talk", type="primary", use_container_width=True)

# Handle Voice Input
if voice_clicked:
    with st.spinner("🎙️ Listening to microphone..."):
        spoken_transcript = listen_to_microphone()
        
    if spoken_transcript:
        # Append user text to chat interface
        st.session_state.messages.append({"role": "user", "text": spoken_transcript})
        
        # Process through RAG chain
        with st.spinner("🧠 Analyzing policy documents and thinking..."):
            ai_reply = generate_voice_response(spoken_transcript)
            
        # Append AI text and trigger spoken output
        st.session_state.messages.append({"role": "assistant", "text": ai_reply})
        speak_text_async(ai_reply)
        st.rerun()
    else:
        st.warning("Could not capture clear audio. Check microphone connection or try again.")

# --- Bottom Interface: Visual Chat Stream ---
st.subheader("💬 Chat Transcript")

# Loop backwards or forwards to draw the messages on screen
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.write(message["text"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.write(message["text"])

# Fallback text entry box for hybrid input option
if text_input := st.chat_input("Or type your policy question here..."):
    st.session_state.messages.append({"role": "user", "text": text_input})
    with st.spinner("🧠 Analyzing policy documents..."):
        ai_reply = generate_voice_response(text_input)
    st.session_state.messages.append({"role": "assistant", "text": ai_reply})
    speak_text_async(ai_reply)
    st.rerun()