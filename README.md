# Video & Audio QA System

This repository contains the code for a Video and Audio QA (Question Answering) System built with Streamlit. The system is designed to provide an interactive interface for users to ask questions about videos and receive answers.

## Directory Structure

The project is organized into the following files:

1. `video_qa_system.ipynb`: A Jupyter notebook that provides a comprehensive overview of the AI pipeline, including video processing, transcription with Whisper, and Q&A with Gemini.
2. `video_qa_app.py`: The main application file, built with Streamlit. This file contains the web app that users interact with.
3. `requirements.txt`: Lists the Python package dependencies required for the project. To install these dependencies, run `pip install -r requirements.txt`.
4. `packages.txt`: Lists system-level dependencies required for deployment on Streamlit Cloud.

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository: `git clone https://github.com/AtaUllahB/Python-Video-Audio-QA-System.git`
2. Navigate to the project directory: `cd Python-Video-Audio-QA-System`
3. Install the Python dependencies: `pip install -r requirements.txt`
4. Create a `.streamlit` directory in the project root if it doesn't already exist.
5. Inside the `.streamlit` directory, create a `secrets.toml` file.
6. Obtain your Gemini API key by following the instructions provided by Gemini. If you haven't already, you'll need to sign up for an account and generate an API key.
7. Add your Gemini API key to the `secrets.toml` file in the following format: GEMINI_API_KEY = "add_key_here"
8. Navigate back to the project root directory `cd..`
9. Run the Streamlit app: `streamlit run video_qa_app.py`

## Deployment

The application is designed to be deployed on Streamlit Cloud.

## Acknowledgments

Streamlit for providing an easy-to-use framework for building web applications.

<img src="https://github.com/AtaUllahB/React-ReCharts/blob/master/recording.gif?raw=true">
