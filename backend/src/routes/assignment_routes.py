from flask import Blueprint, request, jsonify
import os
import logging
import PyPDF2

from src.config.settings import config
from src.services.correction_service import CorrectionService
from src.utils.file_handler import FileHandler

logging.basicConfig(level=logging.DEBUG)
assignment_bp = Blueprint('assignments', __name__)

@assignment_bp.route('/correct', methods=['POST'])
def correct_assignments():
    """
    Endpoint para corrección de tareas
    
    Esperado:
    - Opcional: key_file (Archivo JSON o PDF con criterios)
    - student_files: Archivos de tareas a corregir
    - Opcional: language (Idioma para las respuestas, por defecto "español")
    """
    key_path = None
    student_paths = []
    try:
        # Validar idioma y archivos de entrada
        language = request.form.get("language", "español")
        student_files = request.files.getlist('student_files')
        if not student_files:
            return jsonify({"error": "Se requieren archivos de tareas para corregir"}), 400

        # Procesar archivo clave (opcional)
        key_file = request.files.get('key_file')
        key_criteria = None
        if key_file:
            key_path = FileHandler.save_uploaded_file(key_file, config.UPLOAD_FOLDER)
            if key_file.filename.endswith('.pdf'):
                key_criteria = FileHandler.read_pdf(key_path)
            elif key_file.filename.endswith('.json'):
                key_criteria = FileHandler.read_json(key_path)
            else:
                return jsonify({"error": "Tipo de archivo de clave no soportado"}), 400

        # Leer archivos de tareas
        student_paths = [FileHandler.save_uploaded_file(file, config.UPLOAD_FOLDER) for file in student_files]
        assignments_content = [
            FileHandler.read_pdf(path) if path.endswith('.pdf') else FileHandler.read_text(path)
            for path in student_paths
        ]

        # Corrección
        results = CorrectionService.batch_correction(
            key_criteria,
            assignments_content,
            language=language
        )

        return jsonify({"results": [result.to_dict() for result in results]})

    except Exception as e:
        logging.error(f"Error en el proceso de corrección: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

    finally:
        if key_path:
            FileHandler.clean_temporary_files([key_path])
        FileHandler.clean_temporary_files(student_paths)

# Método para leer PDF
def read_pdf(file_path):
    """
    Read a PDF file and return its text content.
    """
    try:
        with open(file_path, 'rb') as file:  # 'rb' for reading in binary mode
            pdf_reader = PyPDF2.PdfReader(file)
            text = []
            for page in pdf_reader.pages:
                text.append(page.extract_text() if page.extract_text() else "")
            return ' '.join(text).strip()
    except Exception as e:
        logging.error(f"Error reading PDF file at {file_path}: {e}", exc_info=True)
        raise
