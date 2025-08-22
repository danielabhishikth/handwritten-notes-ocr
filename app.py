import streamlit as st
import pytesseract
from PIL import Image
from fpdf import FPDF
import fitz  # pymupdf
import io
def extract_text_from_file(file_path):
    text = ""
    if file_path.lower().endswith((".jpg", ".jpeg", ".png")):
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
    elif file_path.lower().endswith(".pdf"):
        pages = convert_from_path(file_path)
        for page in pages:
            text += pytesseract.image_to_string(page) + "\n\n"
    return tex
  !pip install reportlab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def save_text_to_pdf(text, output_filename="output_notes.pdf"):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter
    y = height - 50
    for line in text.split("\n"):
        c.drawString(50, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50
    c.save()
import streamlit as st

st.set_page_config(page_title="Smart Notes Converter", page_icon="📚", layout="wide")
st.title("📚 Handwritten Notes → Digital PDF Converter")

uploaded_file = st.file_uploader("Upload handwritten notes (JPG/PNG/PDF)", type=["jpg","jpeg","png","pdf"])

if uploaded_file:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("⏳ Processing your file...")
    extracted_text = extract_text_from_file(uploaded_file.name)

    st.subheader("📄 Extracted Text")
    st.text_area("Output", extracted_text, height=300)

    # Save as PDF
    save_text_to_pdf(extracted_text, "digital_notes.pdf")
    with open("digital_notes.pdf", "rb") as f:
        st.download_button("⬇️ Download PDF", f, file_name="digital_notes.pdf")
st.set_page_config(page_title="Smart Notes Converter", page_icon="📝", layout="wide")
st.title("📝 Smart Handwritten Notes Converter")
st.markdown("Convert your handwritten notes into clean, searchable **digital PDFs** in seconds 🚀")
st.header("📤 Upload Your Notes")
st.markdown("""
<style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px 24px;
    }
    .stTextArea textarea {
        background-color: #f9f9f9;
        font-family: 'Courier New', monospace;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)
mode = st.toggle("🌙 Dark Mode")
if mode:
    st.markdown("<style>body{background-color: #121212; color:white}</style>", unsafe_allow_html=True)
