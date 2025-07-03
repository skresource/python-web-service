import os
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
import io

def generate_summary(file_stream, mime_type):
    """
    Extracts text from a file stream based on its MIME type and generates a summary.
    """
    try:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        print("### GEMINI_API_KEY", os.environ["GEMINI_API_KEY"])
        text = ""
        if mime_type == 'application/pdf':
            reader = PdfReader(file_stream)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            doc = Document(file_stream)
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            return "Unsupported file type"

        if not text.strip():
            return "Could not extract text from the file."

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Please provide a concise summary of the following text and if this is a cv or resume point extract the name, email, phone number, total experience and objectives and the past companies the candidate worked for, skills and projects worked on and return the summary in a json format and the return type as Resume with the following keys: name, email, phone, total_experience, objectives, past_companies if not a cv or resume return the summary in a json format, return type as Others with the following keys: heading, summary\n\n{text}")
        print(f"\n\033[94m### RESPONSE\033[0m\n{response.text}")
        return response.text

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Failed to generate summary." 