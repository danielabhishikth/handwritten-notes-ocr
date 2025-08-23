import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import tempfile
import os
import PyPDF2
from fpdf import FPDF

# Initialize OCR reader
reader = easyocr.Reader(['en'])

# Function to extract text from images
def extract_text_from_image(image):
    results = reader.readtext(np.array(image))
    extracted_text = " ".join([res[1] for res in results])
    return extracted_text

# Function to extract text from PDFs
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# Function to save text to PDF
def save_text_to_pdf(text, output_path="output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(output_path)
    return output_path

# Streamlit UI
st.set_page_config(page_title="Handwritten Notes OCR", layout="wide")
st.title("📝 Handwritten Notes OCR")
st.write("Upload handwritten **images (JPG/PNG)** or **PDFs** and get digital text back as a PDF.")

uploaded_file = st.file_uploader("Upload a JPG, PNG, or PDF", type=["jpg", "png", "jpeg", "pdf"])

if uploaded_file is not None:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    extracted_text = ""

    if file_ext in ["jpg", "jpeg", "png"]:
        # Process image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        with st.spinner("Extracting text..."):
            extracted_text = extract_text_from_image(image)

    elif file_ext == "pdf":
        # Save temp PDF and process
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        with st.spinner("Extracting text from PDF..."):
            with open(tmp_path, "rb") as f:
                extracted_text = extract_text_from_pdf(f)
        os.remove(tmp_path)

    if extracted_text.strip():
        st.subheader("📄 Extracted Text")
        st.text_area("Digital Text", extracted_text, height=200)

        if st.button("Download as PDF"):
            output_pdf = save_text_to_pdf(extracted_text)
            with open(output_pdf, "rb") as f:
                st.download_button("⬇ Download PDF", f, file_name="digital_notes.pdf", mime="application/pdf")
    else:
        st.error("No text could be extracted. Please try a clearer image or PDF.")
