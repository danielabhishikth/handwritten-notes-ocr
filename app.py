from flask import Flask, render_template, request, send_file
import easyocr
import os
from werkzeug.utils import secure_filename
from fpdf import FPDF
import fitz  # PyMuPDF for PDFs
import tempfile

app = Flask(__name__)
reader = easyocr.Reader(['en'])

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def ocr_image(path):
    results = reader.readtext(path)
    text = " ".join([res[1] for res in results])
    return text

def ocr_pdf(path):
    doc = fitz.open(path)
    all_text = []
    for page in doc:
        pix = page.get_pixmap()
        img_path = tempfile.mktemp(suffix=".png")
        pix.save(img_path)
        all_text.append(ocr_image(img_path))
        os.remove(img_path)
    return "\n".join(all_text)

def save_text_to_pdf(text, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(output_path)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            extracted = ocr_image(filepath)
        elif filename.lower().endswith(".pdf"):
            extracted = ocr_pdf(filepath)
        else:
            return "Unsupported file type", 400

        output_path = os.path.join(UPLOAD_FOLDER, "output.pdf")
        save_text_to_pdf(extracted, output_path)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
