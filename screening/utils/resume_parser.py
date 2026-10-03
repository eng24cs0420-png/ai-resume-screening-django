from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_resume(file):
    filename = file.name.lower()

    if filename.endswith(".pdf"):
        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    elif filename.endswith(".docx"):
        document = Document(file)
        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    return ""