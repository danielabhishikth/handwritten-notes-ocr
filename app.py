import streamlit as st
import easyocr
import numpy as np
import cv2
from PIL import Image
import PyPDF2
from fpdf import FPDF
import tempfile
import os

# Initialize EasyOCR Reader
reader = easyocr.Reader(["en"], gpu=False)

# OCR for images
def extract_text_from_image(image):
    if isinstance(image, np.ndarray):
        results = reader.readtext(image)
    else:
        image = np.array(image)
        results = reader.readtext(image)

    text = " ".join([res[1] for res in results])
    return text.strip()

# OCR for PDFs
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    for page_num, page in enumerate(pdf_reader.pages):
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
        else:
            # Fallback to OCR if text is missing (scanned PDF)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
                xObject = page.get("/Resources", {}).get("/XObject", {})
                if xObject:
                    for obj in xObject:
                        if xObject[obj]["/Subtype"] == "/Image":
                            size = (xObject[obj]["/Width"], xObject[obj]["/Height"])
                            data = xObject[obj].get_data()
                            img = Image.frombytes("RGB", size, data)
                            img.save(tmp_img.name, "JPEG")
                            text += extract_text_from_image(img) + "\n"
                            os.remove(tmp_img.name)
    return text.strip()

# Save extracted text into a PDF
def save_text_to_pdf(text, output_filename="output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(output_filename)
    return output_filename

# Streamlit UI
st.set_page_config(page_title="Handwritten Notes OCR", layout="centered")

st.markdown("<h1 style='text-align: center;'>📝 Handwritten Notes to PDF</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📂 Upload Image (JPG/PNG) or PDF", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file is not None:
    extracted_text = ""

    if uploaded_file.type in ["image/jpeg", "image/png"]:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        extracted_text = extract_text_from_image(image)

    elif uploaded_file.type == "application/pdf":
        extracted_text = extract_text_from_pdf(uploaded_file)

    if extracted_text:
        st.subheader("📖 Extracted Text")
        st.text_area("Output", extracted_text, height=250)

        output_pdf = save_text_to_pdf(extracted_text)
        with open(output_pdf, "rb") as f:
            st.download_button("⬇ Download as PDF", f, file_name="converted_notes.pdf")
    else:
        st.error("❌ Could not extract any text. Try another file.")
