import os
import streamlit as st
from pytube import YouTube
from chat_management import add_message
from transcription import transcribe_audio
from pytube.exceptions import RegexMatchError
from moviepy.editor import VideoFileClip, AudioFileClip

def save_uploaded_file(uploaded_file):
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    file_path = 'temp_file' + file_extension
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.read())
    return file_path

def extract_file_audio(video_file_path):
    audio_file_path = 'audio_file.mp3'
    video_clip = VideoFileClip(video_file_path)
    video_clip.audio.write_audiofile(audio_file_path)
    video_clip.close()
    os.remove(video_file_path)
    return audio_file_path

def process_uploaded_file(uploaded_file):
    with st.status("Processing file...", expanded=True) as status:
        file_path = save_uploaded_file(uploaded_file)
        st.write("Converting video to audio")
        audio_file_path = extract_file_audio(file_path)
        st.write("Transcribing audio")
        text = transcribe_audio(audio_file_path)
        add_message("assistant", f"Transcribed Text: {text}")
        st.session_state.file_processed = True
        status.update(label="Processing complete!", state="complete", expanded=False)

def extract_youtube_audio(video_file_path):
    audio_file_path = 'audio_file.mp3'
    audio_clip = AudioFileClip(video_file_path)
    audio_clip.write_audiofile(audio_file_path)
    audio_clip.close()
    os.remove(video_file_path)
    return audio_file_path

def download_youtube_video(youtube_url):
    try:
        yt = YouTube(youtube_url)
        video = yt.streams.filter(only_audio=True).first()
        video_file_path = 'temp_video.mp4'
        video.download(filename=video_file_path)
        return video_file_path
    except RegexMatchError as e:
        st.error("Please enter a valid YouTube URL.")

def process_youtube_url(youtube_url):
    with st.status("Processing URL...", expanded=True) as status:
        st.write("Fetching video from YouTube")
        file_path = download_youtube_video(youtube_url)
        if file_path is None:
            return None
        st.write("Converting video to audio")
        audio_file_path = extract_youtube_audio(file_path)
        st.write("Transcribing audio")
        text = transcribe_audio(audio_file_path)
        add_message("assistant", f"Transcribed Text: {text}")
        st.session_state.file_processed = True
        status.update(label="Processing complete!", state="complete", expanded=False)
