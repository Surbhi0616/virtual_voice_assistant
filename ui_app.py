import streamlit as st
import os
from llm_generation import generate_voice_response
from rag_backend import initialize_knowledge_base, query_knowledge_base
import speech_recognition as sr # Note: Keep this for local use, ignore in cloud

# Initialize the RAG system once
@st.cache_resource
def get_db():
    return initialize_knowledge_base()

st.title("🎙️ Virtual Voice Claims Assistant")

db = get_db()
input_method = st.radio("Choose Input Method:", ("Text Input", "Upload Audio File"))

user_query = None

if input_method == "Text Input":
    user_query = st.text_input("Ask a question about the policy:")
else:
    audio_file = st.file_uploader("Upload audio file", type=["wav"])
    if audio_file:
        st.write("Transcribing...")
        # Simple transcription logic using the uploaded file
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            try:
                user_query = recognizer.recognize_google(audio_data)
                st.write(f"Transcribed: {user_query}")
            except Exception as e:
                st.error("Could not transcribe audio.")

if user_query:
    st.write(f"Searching for: {user_query}")
    # RAG Search
    results = query_knowledge_base(user_query, db)
    
    # Generate Response
    response = generate_voice_response(user_query, results)
    
    st.subheader("Response:")
    st.write(response)