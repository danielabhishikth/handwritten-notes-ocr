import streamlit as st
import easyocr
from pdf2image import convert_from_path
from PIL import Image
import tempfile
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Initialize EasyOCR Reader (English, add more langs if needed)
reader = easyocr.Reader(['en'])

# Function: Extract text from image
def extract_text_from_image(image):
    results = reader.readtext(image)
    text = "\n".join([res[1] for res in results])
    return text

# Function: Convert text to PDF
def save_text_as_pdf(text, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    y = height - 40
    for line in text.split("\n"):
        c.drawString(40, y, line)
        y -= 15
        if y < 40:
            c.showPage()
            y = height - 40
    c.save()

# Streamlit UI
st.set_page_config(page_title="Handwritten Notes OCR", layout="centered")
st.markdown("<h2 style='text-align: center; color: #4CAF50;'>📝 Handwritten Notes to Digital Text</h2>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your handwritten notes (JPG, PNG, PDF)", type=["jpg", "png", "pdf"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()

    extracted_text = ""

    with tempfile.NamedTemporaryFile(delete=False, suffix="." + file_type) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    if file_type == "pdf":
        pages = convert_from_path(tmp_path)
        for page in pages:
            extracted_text += extract_text_from_image(page) + "\n"
    else:
        image = Image.open(tmp_path)
        extracted_text = extract_text_from_image(image)

    st.subheader("📄 Extracted Text")
    st.text_area("Output", extracted_text, height=200)

    # Save extracted text as PDF
    if st.button("Download as PDF"):
        pdf_path = "output_notes.pdf"
        save_text_as_pdf(extracted_text, pdf_path)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name="handwritten_notes.pdf", mime="application/pdf")

    os.remove(tmp_path)
