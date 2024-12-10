from flask import Blueprint, request, jsonify
import logging
from concurrent.futures import ThreadPoolExecutor

from src.config.settings import config
from src.services.correction_service import CorrectionService
from src.utils.file_handler import FileHandler
from src.utils.analysis import Analysis
from src.services.file_processor import FileProcessor  # Para procesar texto e imágenes

logging.basicConfig(level=logging.DEBUG)
assignment_bp = Blueprint('assignments', __name__)

@assignment_bp.route('/correct', methods=['POST'])
def correct_assignments():
    """
    Endpoint para corrección de tareas con validación de ejercicios, análisis de imágenes y detección de similitudes.

    Esperado:
    - Opcional: key_file (Archivo JSON o PDF con criterios)
    - student_files: Archivos de tareas a corregir
    - Opcional: language (Idioma para las respuestas, por defecto "español")
    - Opcional: required_exercises (Lista de ejercicios requeridos)
    """
    key_path = None
    student_paths = []
    try:
        # Validar idioma y parámetros de entrada
        language = request.form.get("language", "español").strip().lower()
        model_type = request.form.get("model_type", "gpt-4").strip().lower()
        required_exercises = request.form.getlist("required_exercises")
        student_files = request.files.getlist('student_files')
        if not student_files:
            return jsonify({"error": "Se requieren archivos de tareas para corregir"}), 400

        # Procesar archivo clave (opcional)
        key_file = request.files.get('key_file')
        key_criteria = None
        if key_file:
            key_path = FileHandler.save_uploaded_file(key_file, config.UPLOAD_FOLDER)
            key_criteria = FileHandler.read_file(key_path)

        # Procesar archivos de tareas
        student_paths = [FileHandler.save_uploaded_file(file, config.UPLOAD_FOLDER) for file in student_files]
        assignments = [FileProcessor.extract_text(path) for path in student_paths]

        corrections = []

        # Validación y corrección de cada tarea
        for idx, assignment in enumerate(assignments):
            correction_service = CorrectionService(model_type)
            correction_result = correction_service.correct_assignment_with_validation(
                key_criteria=key_criteria,
                assignment_content=assignment,
                required_exercises=required_exercises,
                language=language
            )
            corrections.append({
                "student_file": student_files[idx].filename,
                "result": correction_result
            })

        # Detección de similitudes entre archivos
        similarity_results = []
        for i in range(len(assignments)):
            for j in range(i + 1, len(assignments)):
                similarity = Analysis.detect_similarity(assignments[i], assignments[j])
                similarity_results.append({
                    "file1": student_files[i].filename,
                    "file2": student_files[j].filename,
                    "similarity_percentage": round(similarity, 2)
                })

        # Construir respuesta
        response = {
            "corrections": corrections,
            "similarities": similarity_results
        }

        return jsonify(response)

    except Exception as e:
        logging.error(f"Error en el proceso de corrección: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

    finally:
        # Limpiar archivos temporales
        if key_path:
            FileHandler.clean_temporary_files([key_path])
        FileHandler.clean_temporary_files(student_paths)
