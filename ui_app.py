import streamlit as st
from streamlit_audiorecorder import audiorecorder
from llm_generation import generate_voice_response
from rag_backend import initialize_knowledge_base, query_knowledge_base

st.title("🗣️ Voice Claims Assistant")

# Initialize your RAG system
db = initialize_knowledge_base()

# Browser-based Audio Recorder
audio = audiorecorder("Click to Record", "Recording...")

if len(audio) > 0:
    st.audio(audio.export().read()) # Play back the recording
    
    # Process the audio file directly using a library like SpeechRecognition
    # (Since the file is now in memory, it will work!)
    import speech_recognition as sr
    import io
    
    recognizer = sr.Recognizer()
    # Convert audio object to a file-like object
    audio_file = io.BytesIO(audio.export().read())
    
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text_query = recognizer.recognize_google(audio_data)
            st.write(f"**You said:** {text_query}")
            
            # Perform RAG Search
            results = query_knowledge_base(text_query, db)
            
            # Generate Response
            response = generate_voice_response(text_query, results)
            st.write(f"**Assistant:** {response}")
            
        except Exception as e:
            st.error("Could not transcribe your voice.")