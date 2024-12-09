import logging
import os
import uuid
from werkzeug.utils import secure_filename
import json
import PyPDF2
import time

class FileHandler:
    """
    Utility class for handling file operations
    """
    @staticmethod
    def generate_unique_filename(filename):
        """
        Generate a unique filename to prevent overwriting
        """
        unique_id = str(uuid.uuid4())
        return f"{unique_id}_{secure_filename(filename)}"

    @staticmethod
    def save_uploaded_file(file, upload_folder):
        """
        Save an uploaded file with a unique name
        
        :param file: File object from the request
        :param upload_folder: Directory to save the file
        :return: Path to the saved file
        """
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        filename = FileHandler.generate_unique_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return file_path
    
    @staticmethod
    def read_file(file_path):
        """
        Lee el contenido del archivo, soportando PDF, texto y JSON.
        """
        if file_path.endswith(".pdf"):
            return FileHandler.read_pdf(file_path)
        elif file_path.endswith(".json"):
            return FileHandler.read_json(file_path)
        else:
            return FileHandler.read_text(file_path)

    @staticmethod
    def read_json(file_path):
        """
        Read a JSON file and return its content as a dictionary
        
        :param file_path: Path to the JSON file
        :return: Dictionary with the content of the JSON file
        """
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file at {file_path} does not exist.")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in the file {file_path}.")

    @staticmethod
    def read_text(file_path):
        """
        Read a text file and return its contents as a string
        
        :param file_path: Path to the text file
        :return: String with the content of the text file
        """
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"The file at {file_path} does not exist.")
        except IOError:
            raise IOError(f"Unable to read the file {file_path}.")

    @staticmethod
    def read_pdf(file_path):
        """
        Read a PDF file and return its text content.
        
        :param file_path: Path to the PDF file
        :return: String containing all text extracted from the PDF
        """
        try:
            with open(file_path, 'rb') as file:  # 'rb' for reading in binary mode
                pdf_reader = PyPDF2.PdfReader(file)
                text = []
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
                return ' '.join(text)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file at {file_path} does not exist.")
        except Exception as e:
            raise IOError(f"Could not read the PDF file: {e}")
        
    @staticmethod
    def clean_temporary_files(file_paths):
        """
        Remove specified temporary files
        
        :param file_paths: List of file paths to delete
        """
        for file_path in file_paths:
            try:
                os.remove(file_path)
                logging.info(f"Archivo eliminado: {file_path}")
            except Exception as e:
                logging.error(f"Error eliminando archivo {file_path}: {e}")