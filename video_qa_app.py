import os
import whisper
import streamlit as st
import google.generativeai as genai
from moviepy.editor import VideoFileClip, AudioFileClip
from pytube import YouTube

# Title of the application
st.title("Video & Audio Based Chatbot")

# Initialize chat history and file processed flag
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file_processed" not in st.session_state:
    st.session_state.file_processed = False

# Choose between uploading a file or entering a YouTube URL
input_option = st.radio("Choose your input method:", ("Upload a file", "Enter YouTube URL"))

if input_option == "Upload a file":
    # File uploader for video and audio files
    uploaded_file = st.file_uploader("Upload a video or audio file", type=["avi", "mkv", "mov", "mp4", "mp3", "wav"])

    # Button to process file
    if st.button("Process File"):
        if uploaded_file is not None:
            # Display status message indicating processing has started
            with st.status("Processing file...", expanded=True) as status:
                
                # Check extension to determine type of file
                file_extension = os.path.splitext(uploaded_file.name)[1].lower()
                if file_extension in [".avi", ".mkv", ".mov", ".mp4"]:
                    
                    # Process video file
                    video_bytes = uploaded_file.read()
                    video_file_path = 'temp_video.mp4'
                    
                    with open(video_file_path, 'wb') as f:
                        f.write(video_bytes)
                    audio_file_path = 'audio_file.mp3'
                    
                    # Update status
                    st.write("Converting video to audio")
                    
                    # Extract audio from video
                    video_clip = VideoFileClip(video_file_path)
                    video_clip.audio.write_audiofile(audio_file_path)
                    video_clip.close()
                    os.remove(video_file_path)
                
                elif file_extension in [".mp3", ".wav"]:
                    # Process audio file directly
                    audio_bytes = uploaded_file.read()
                    audio_file_path = 'audio_file' + file_extension
                    
                    with open(audio_file_path, 'wb') as f:
                        f.write(audio_bytes)
                
                # Update status
                st.write("Transcribing audio")
                
                # Transcribe audio with Whisper
                whisper_model = whisper.load_model("base")
                result = whisper_model.transcribe(audio_file_path)
                text = result["text"]
                
                # Save the transcribed text to a file
                with open("transcribed_text.txt", "w", encoding="utf-8") as f:
                    f.write(text)
                os.remove(audio_file_path)
                
                # Add transcribed text to chat history
                st.session_state.messages.append({"role": "assistant", "content": f"Transcribed Text: {text}"})
                
                # Update status
                status.update(label="Processing complete!", state="complete", expanded=False)
                
                # Set the file processed flag to True
                st.session_state.file_processed = True
        else:
            st.session_state.messages.append({"role": "assistant", "content": "Please upload a file."})

elif input_option == "Enter YouTube URL":
    # Input field for YouTube URL
    youtube_url = st.text_input("Enter YouTube video URL:")

    # Button to process file
    if st.button("Process URL"):
        if youtube_url:
            # Display status message indicating processing has started
            with st.status("Processing URL...", expanded=True) as status:

                # Update status
                st.write("Fetching video from YouTube")
                
                # Download YouTube video
                yt = YouTube(youtube_url)
                video = yt.streams.filter(only_audio=True).first()
                video_file_path = 'temp_video.mp4'
                video.download(filename=video_file_path)

                # Update status
                st.write("Converting video to audio")
                
                # Extract audio from video
                audio_file_path = 'audio_file.mp3'
                audio_clip = AudioFileClip(video_file_path)
                audio_clip.write_audiofile(audio_file_path)
                os.remove(video_file_path)

                # Update status
                st.write("Transcribing audio")

                # Transcribe audio with Whisper
                whisper_model = whisper.load_model("base")
                result = whisper_model.transcribe(audio_file_path)
                text = result["text"]
                    
                # Save the transcribed text to a file
                with open("transcribed_text.txt", "w", encoding="utf-8") as f:
                    f.write(text)
                os.remove(audio_file_path)
                
                # Add transcribed text to chat history
                st.session_state.messages.append({"role": "assistant", "content": f"Transcribed Text: {text}"})

                # Update status
                status.update(label="Processing complete!", state="complete", expanded=False)

                # Set the file processed flag to True
                st.session_state.file_processed = True
        else:
            st.session_state.messages.append({"role": "assistant", "content": "Please enter a YouTube URL."})

# Accept user input as a chat message
if prompt := st.chat_input("Enter question:"):
    # Check if the file has been processed
    if not st.session_state.file_processed:
        st.session_state.messages.append({"role": "assistant", "content": "Process the file first."})
        
    else:
        # Read the transcribed text from the file
        try:
            with open("transcribed_text.txt", "r", encoding="utf-8") as f:
                transcribed_text = f.read()
        except FileNotFoundError:
            st.session_state.messages.append({"role": "assistant", "content": "Please upload a file and process it first"})
        
        # Q&A with Gemini
        gemini_api_key = st.secrets["GEMINI_API_KEY"]
        
        genai.configure(api_key=gemini_api_key)
        gemini_model = genai.GenerativeModel('gemini-pro')
        
        context = transcribed_text
        response = gemini_model.generate_content(f"{context}\n{prompt}")
        
        # Add user's question to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response.text})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
