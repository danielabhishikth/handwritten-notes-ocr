import streamlit as st
import easyocr
import numpy as np
import cv2
from PIL import Image
from fpdf import FPDF
import PyPDF2
import tempfile

# OCR reader
reader = easyocr.Reader(['en'])

def extract_text_from_image(image):
    results = reader.readtext(np.array(image))
    text = " ".join([res[1] for res in results])
    return text

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""  # Fallback if page has no text
    return text

def save_text_as_pdf(text, filename="output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)
    return filename

# --- Streamlit UI ---
st.title("📝 Handwritten Notes OCR to Digital PDF")

uploaded_file = st.file_uploader("Upload JPG/PNG/PDF", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file:
    file_type = uploaded_file.type

    if "pdf" in file_type:
        st.info("Extracting text from PDF...")
        extracted_text = extract_text_from_pdf(uploaded_file)

    else:  # image
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_column_width=True)
        extracted_text = extract_text_from_image(image)

    # Display extracted text
    st.subheader("Extracted Text:")
    st.text_area("Text", extracted_text, height=200)

    if st.button("Download as PDF"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf_path = save_text_as_pdf(extracted_text, tmp.name)
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download PDF", f, file_name="output.pdf")
