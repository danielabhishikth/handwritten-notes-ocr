import streamlit as st
import pymudf
import numpy as np
import cv2
from easyocr import Reader
from fpdf import FPDF
from PIL import Image

# Initialize EasyOCR reader
reader = Reader(['en'])

# Function: Extract text from images
def extract_text_from_image(uploaded_file):
    image = Image.open(uploaded_file)
    img = np.array(image)

    results = reader.readtext(img)
    extracted_text = " ".join([res[1] for res in results])

    return extracted_text

# Function: Extract text from PDFs using PyMuPDF
def extract_text_from_pdf(uploaded_file):
    text_results = []

    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        pix = page.get_pixmap()
        img_bytes = pix.tobytes("png")

        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        results = reader.readtext(img)
        extracted_text = " ".join([res[1] for res in results])
        text_results.append(extracted_text)

    return "\n\n".join(text_results)

# Function: Save extracted text to a PDF
def save_text_to_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    return pdf.output(dest="S").encode("latin-1")

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Handwritten Notes OCR", layout="centered")

st.title("📝 Handwritten Notes OCR")
st.markdown("Upload your **handwritten notes (jpg, png, or pdf)** and get back clean, digital text.")

uploaded_file = st.file_uploader("Upload your file", type=["jpg", "png", "pdf"])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        st.info("📄 Processing PDF...")
        extracted_text = extract_text_from_pdf(uploaded_file)
    else:
        st.info("🖼️ Processing Image...")
        extracted_text = extract_text_from_image(uploaded_file)

    if extracted_text.strip():
        st.subheader("✅ Extracted Text")
        st.write(extracted_text)

        pdf_bytes = save_text_to_pdf(extracted_text)
        st.download_button("📥 Download as PDF", data=pdf_bytes, file_name="extracted_text.pdf", mime="application/pdf")
    else:
        st.error("❌ No text detected. Try uploading a clearer image or handwritten notes.")
