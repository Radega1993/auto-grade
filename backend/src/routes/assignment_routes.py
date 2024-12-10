from flask import Blueprint, request, jsonify
import logging
from concurrent.futures import ThreadPoolExecutor
from difflib import SequenceMatcher

from src.config.settings import config
from src.services.correction_service import CorrectionService
from src.utils.file_handler import FileHandler

logging.basicConfig(level=logging.DEBUG)
assignment_bp = Blueprint('assignments', __name__)

@assignment_bp.route('/correct', methods=['POST'])
def correct_assignments():
    """
    Endpoint para corrección de tareas con paralelización y detección de similitudes.

    Esperado:
    - Opcional: key_file (Archivo JSON o PDF con criterios)
    - student_files: Archivos de tareas a corregir
    - Opcional: language (Idioma para las respuestas, por defecto "español")
    """
    key_path = None
    student_paths = []
    try:
        # Validar idioma y archivos de entrada
        language = request.form.get("language", "español").strip().lower()
        model_type = request.form.get("model_type", "gpt-3.5-turbo").strip().lower()
        student_files = request.files.getlist('student_files')
        if not student_files:
            return jsonify({"error": "Se requieren archivos de tareas para corregir"}), 400

        # Procesar archivo clave (opcional)
        key_file = request.files.get('key_file')
        key_criteria = None
        if key_file:
            key_path = FileHandler.save_uploaded_file(key_file, config.UPLOAD_FOLDER)
            key_criteria = FileHandler.read_file(key_path)

        # Leer y procesar archivos de tareas
        student_paths = [FileHandler.save_uploaded_file(file, config.UPLOAD_FOLDER) for file in student_files]
        assignments = [FileHandler.read_file(path) for path in student_paths]

        # Caching de resultados para tareas idénticas
        results_cache = {}
        corrections = []

        # Corrección con reducción de costos
        for idx, assignment in enumerate(assignments):
            if assignment in results_cache:
                logging.info(f"Tarea {student_files[idx].filename} recuperada del cache.")
                corrections.append(results_cache[assignment])
            else:
                correction_result = CorrectionService(model_type).correct_assignment_with_ai_detection(
                    key_criteria, assignment, language
                )
                corrections.append(correction_result)
                results_cache[assignment] = correction_result

        # Detección de similitudes entre archivos
        similarity_results = []
        for i in range(len(assignments)):
            for j in range(i + 1, len(assignments)):
                similarity = SequenceMatcher(None, assignments[i], assignments[j]).ratio()
                similarity_results.append({
                    "file1": student_files[i].filename,
                    "file2": student_files[j].filename,
                    "similarity_percentage": round(similarity * 100, 2)
                })

        # Construir respuesta
        response = {
            "corrections": [
                {
                    "student_file": student_files[i].filename,
                    "result": corrections[i]
                }
                for i in range(len(corrections))
            ],
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