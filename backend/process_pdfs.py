import os
from utils.pdf_processing import extract_text_with_ocr, filter_unwanted_content
from utils.database import connect_to_database

BASE_FOLDER = r"D:\Manish\Personal\TNPSC\Books"
POPPLER_PATH = r"C:\poppler\poppler-25.11.0\Library\bin"

def save_to_database(grade, term, subject, content):
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO extracted_content (grade, term, subject, content)
            VALUES (%s, %s, %s, %s)
        """, (grade, term, subject, content))
        connection.commit()
        connection.close()

def process_pdfs():
    for grade_folder in os.listdir(BASE_FOLDER):
        grade_path = os.path.join(BASE_FOLDER, grade_folder)
        if not os.path.isdir(grade_path):
            continue

        grade = int(grade_folder.replace("th", "").strip())

        for term_folder in os.listdir(grade_path):
            term_path = os.path.join(grade_path, term_folder)
            if not os.path.isdir(term_path):
                continue

            term = int(term_folder.replace("Term", "").strip())

            for pdf_file in os.listdir(term_path):
                if not pdf_file.endswith(".pdf"):
                    continue

                subject = pdf_file.replace(".pdf", "").strip()
                file_path = os.path.join(term_path, pdf_file)

                print(f"Processing: Grade {grade}, Term {term}, Subject {subject}")

                # Extract text from the PDF
                extracted_text = extract_text_with_ocr(file_path, POPPLER_PATH)
                # Clean the extracted text
                filtered_text = filter_unwanted_content(extracted_text)
                # Save to the database
                save_to_database(grade, term, subject, filtered_text)

if __name__ == "__main__":
    process_pdfs()