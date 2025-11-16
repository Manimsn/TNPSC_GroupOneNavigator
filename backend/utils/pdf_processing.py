import re
from pdf2image import convert_from_path
from pytesseract import image_to_string

# Configure Tesseract path
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_with_ocr(filepath, poppler_path):
    try:
        images = convert_from_path(filepath, poppler_path=poppler_path)
        text = ""
        for i, image in enumerate(images):
            page_text = image_to_string(image, lang='eng')
            text += f"--- Page {i + 1} ---\n{page_text}\n"
        return text
    except Exception as e:
        print(f"Error with OCR: {e}")
        return ""

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