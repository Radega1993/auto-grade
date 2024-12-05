from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

from src.config.settings import config
from src.services.correction_service import CorrectionService
from src.utils.file_handler import FileHandler

assignment_bp = Blueprint('assignments', __name__)

@assignment_bp.route('/correct', methods=['POST'])
def correct_assignments():
    """
    Endpoint para corrección de tareas
    
    Esperado:
    - key_file: Archivo JSON con criterios
    - student_files: Archivos de tareas a corregir
    """
    try:
        # Validar archivos recibidos
        if 'key_file' not in request.files or 'student_files' not in request.files:
            return jsonify({"error": "Archivos incompletos"}), 400

        key_file = request.files['key_file']
        student_files = request.files.getlist('student_files')

        # Guardar archivos
        key_path = FileHandler.save_file(key_file, config.UPLOAD_FOLDER)
        student_paths = [
            FileHandler.save_file(file, config.UPLOAD_FOLDER) 
            for file in student_files
        ]

        # Leer criterios
        key_criteria = FileHandler.read_json(key_path)

        # Leer contenidos de tareas
        assignments_content = [
            FileHandler.read_text(path) for path in student_paths
        ]

        # Corregir tareas
        results = CorrectionService.batch_correction(
            key_criteria, 
            assignments_content
        )

        # Limpiar archivos temporales
        FileHandler.cleanup_files([key_path] + student_paths)

        return jsonify({
            "results": [result.to_dict() for result in results]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500