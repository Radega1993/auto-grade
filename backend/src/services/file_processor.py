import pytesseract
from pdf2image import convert_from_path
from docx import Document
import logging

class FileProcessor:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """Extrae texto y aplica OCR a imágenes en un PDF."""
        try:
            images = convert_from_path(pdf_path)
            text = []
            for img in images:
                text.append(pytesseract.image_to_string(img, lang="eng"))
            return ' '.join(text)
        except Exception as e:
            logging.error(f"Error al procesar PDF {pdf_path}: {e}")
            return ""

    @staticmethod
    def extract_text_from_word(docx_path: str) -> str:
        """Extrae texto y aplica OCR a imágenes en un documento Word."""
        try:
            doc = Document(docx_path)
            text = []
            for p in doc.paragraphs:
                text.append(p.text)
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text.append(cell.text)
            return '\n'.join(text)
        except Exception as e:
            logging.error(f"Error al procesar Word {docx_path}: {e}")
            return ""

    @staticmethod
    def extract_text(file_path: str) -> str:
        """Determina el tipo de archivo y extrae el texto correspondiente."""
        if file_path.endswith(".pdf"):
            return FileProcessor.extract_text_from_pdf(file_path)
        elif file_path.endswith(".docx"):
            return FileProcessor.extract_text_from_word(file_path)
        elif file_path.endswith(".txt"):
            with open(file_path, 'r') as file:
                return file.read()
        else:
            return ""
