import streamlit as st
from transcription import set_context
from generative_model import get_model
from report_generation import generate_pdf
from chat_management import add_message, display_messages
from file_handling import process_uploaded_file, process_youtube_url

st.title("Video & Audio Based Chatbot")
input_option = st.radio("Choose your input method:", ("Upload a file", "Enter YouTube URL"))

if input_option == "Upload a file":
    uploaded_file = st.file_uploader("Upload a video or audio file", type=["avi", "mkv", "mov", "mp4", "mp3", "wav"])
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Process File"):
            if uploaded_file is not None:
                process_uploaded_file(uploaded_file)
            else:
                st.error("No file uploaded. Please upload a file first.")
    with col2:
        if st.button("Generate Comprehensive Report"):
            generate_pdf()

elif input_option == "Enter YouTube URL":
    youtube_url = st.text_input("Enter YouTube video URL:")
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Process URL"):
            if youtube_url:
                process_youtube_url(youtube_url)
            else:
                st.error("No URL detected. Please enter a YouTube URL first.")
    with col2:
        if st.button("Generate Comprehensive Report"):
            generate_pdf()

if prompt := st.chat_input("Enter question:"):
    if "file_processed" not in st.session_state:
        st.error("No file processed. Please process a file first.")
    else:
        prompt_with_context = set_context(prompt)
        gemini_model = get_model()
        response = gemini_model.generate_content(prompt_with_context)
        try:
            response_text = response.text
        except AttributeError:
            response_text = "Sorry, I couldn't generate a response."
        add_message("user", prompt)
        add_message("assistant", response_text)

display_messages()
