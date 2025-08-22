import streamlit as st
import easyocr
from PIL import Image
import fitz  # PyMuPDF
from fpdf import FPDF
import os

# Add custom CSS for UI
st.markdown("""
    <style>
    body {
        background-color: #f9f9f9;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        font-size: 16px;
        padding: 10px 24px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize EasyOCR
reader = easyocr.Reader(['en'])

st.title("📝 Handwritten Notes to Digital Text")
st.write("Upload handwritten notes (JPG, PNG, or PDF) → Extract text → Download results as PDF.")

# OCR Function
def extract_text_from_file(file_path):
    result = reader.readtext(file_path, detail=0)
    return "\n".join(result)

# Save text to PDF
def save_text_as_pdf(text, filename="output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)
    return filename

# File Upload
uploaded_file = st.file_uploader("Upload a handwritten note (JPG, PNG, or PDF)", type=["jpg", "png", "pdf"])

if uploaded_file:
    file_path = uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    extracted_text = ""

    if uploaded_file.type == "application/pdf":
        st.info("📑 Processing PDF...")
        pdf_doc = fitz.open(file_path)
        for page_num in range(len(pdf_doc)):
            page = pdf_doc.load_page(page_num)
            pix = page.get_pixmap()
            img_path = f"page_{page_num}.png"
            pix.save(img_path)
            extracted_text += extract_text_from_file(img_path) + "\n\n"
            os.remove(img_path)
    else:
        st.image(Image.open(file_path), caption="Uploaded Image", use_container_width=True)
        extracted_text = extract_text_from_file(file_path)

    # Show extracted text
    st.subheader("📄 Extracted Text:")
    st.text_area("Extracted Notes", extracted_text, height=250)

    # Save as PDF
    if extracted_text.strip():
        pdf_filename = save_text_as_pdf(extracted_text)
        with open(pdf_filename, "rb") as pdf_file:
            st.download_button("⬇️ Download as PDF", pdf_file, file_name="digital_notes.pdf", mime="application/pdf")
