# Helper functions
import re
import PyPDF2 as pdf
from io import BytesIO
import markdown2
from xhtml2pdf import pisa
import requests
import google.generativeai as genai
import os

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip().lower())

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    return "".join(page.extract_text() for page in reader.pages if page.extract_text())

def export_pdf(text, filename="output_analysis.pdf"):
    buffer = BytesIO()
    html = markdown2.markdown(text)
    pisa_status = pisa.CreatePDF(src=html, dest=buffer)
    if pisa_status.err:
        raise Exception("PDF generation failed")
    buffer.seek(0)
    return buffer

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def get_gemini_response(prompt, pdf_text, job_description):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-2.5-flash')
    full_prompt = f"{prompt}\n\nResume:\n{pdf_text}\n\nJob Description:\n{job_description}"
    response = model.generate_content(full_prompt)
    return response.text.strip()
