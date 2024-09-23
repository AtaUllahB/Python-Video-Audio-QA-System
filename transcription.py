import os
import whisper
import streamlit as st

def save_transcribed_text(text):
    with open("transcribed_text.txt", "w", encoding="utf-8") as f:
        f.write(text)

def transcribe_audio(audio_file_path):
    whisper_model = whisper.load_model("base")
    result = whisper_model.transcribe(audio_file_path)
    text = result["text"]
    save_transcribed_text(text)
    os.remove(audio_file_path)
    return text

def read_transcribed_text():
    try:
        with open("transcribed_text.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error("No transcribed text available. Please upload and process a file first.")
        return None

def set_context(prompt):
    transcribed_text = read_transcribed_text()
    prompt = f"{transcribed_text}\n{prompt}"
    return prompt
