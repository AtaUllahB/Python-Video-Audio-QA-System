from fpdf import FPDF
import streamlit as st
from generative_model import get_model
from transcription import read_transcribed_text

def generate_pdf():
    # Ensure there is transcribed text available
    transcribed_text = read_transcribed_text()
    if not transcribed_text:
        return

    # Prepare model prompts
    summary_prompt = "Write a summary for the following text:"
    points_prompt = "List the 10 most important points from the following text:"
    qa_prompt = "Generate 10 questions and their answers based on the following text:"

    # Generate responses using the model
    gemini_model = get_model()
    summary_response = gemini_model.generate_content(f"{transcribed_text}\n{summary_prompt}")
    points_response = gemini_model.generate_content(f"{transcribed_text}\n{points_prompt}")
    qa_response = gemini_model.generate_content(f"{transcribed_text}\n{qa_prompt}")

    # Prepare PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)

    # Adding Summary
    pdf.cell(0, 10, 'Summary:', 0, 1)
    pdf.multi_cell(0, 10, summary_response.text)
    pdf.ln(10)  # Add a line break

    # Adding Important Points
    pdf.cell(0, 10, 'Important Points:', 0, 1)
    pdf.multi_cell(0, 10, points_response.text)
    pdf.ln(10)  # Add a line break

    # Adding Q&A
    pdf.cell(0, 10, 'Questions and Answers:', 0, 1)
    pdf.multi_cell(0, 10, qa_response.text)

    # Save PDF
    pdf_file_path = "Comprehensive_Report.pdf"
    try:
        pdf.output(pdf_file_path, 'F')
    except UnicodeEncodeError as e:
        st.error("An encoding error occurred.")

    with open("Comprehensive_Report.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    # Streamlit download button
    st.download_button(
        label="Download Report",
        data=PDFbyte,
        file_name="Comprehensive_Report.pdf",
        mime="application/octet-stream"
    )
