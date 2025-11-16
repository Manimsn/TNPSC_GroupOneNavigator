from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import re

# Create the Flask app instance
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Function to extract text using OCR
def extract_text_with_ocr(filepath):
    try:
        images = convert_from_path(filepath, poppler_path=r'C:\poppler\poppler-25.11.0\Library\bin')
        text = ""
        for i, image in enumerate(images):
            page_text = pytesseract.image_to_string(image)
            text += f"--- Page {i + 1} ---\n{page_text}\n"
        return text
    except Exception as e:
        print(f"Error with OCR: {e}")
        return ""

# Function to filter unwanted content
def filter_unwanted_content(text):
    lines = text.split('\n')
    filtered_lines = []
    for line in lines:
        line = line.strip()
        if not line or "www" in line.lower() or "NOTES" in line or "Page" in line:
            continue
        line = re.sub(r'[^a-zA-Z0-9\s.,]', '', line)
        filtered_lines.append(line)
    return "\n".join(filtered_lines)

# Route to upload PDF
@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        extracted_text = extract_text_with_ocr(filepath)
        filtered_text = filter_unwanted_content(extracted_text)
        return jsonify({"filename": filename, "content": filtered_text}), 200

if __name__ == '__main__':
    app.run(debug=True)