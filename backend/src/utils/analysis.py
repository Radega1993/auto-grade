from difflib import SequenceMatcher
import json
import logging

from src.services.file_processor import FileProcessor

class Analysis:
    @staticmethod
    def detect_similarity(content1: str, content2: str) -> float:
        """Calcula el porcentaje de similitud entre dos contenidos."""
        return SequenceMatcher(None, content1, content2).ratio() * 100

    @staticmethod
    def detect_missing_exercises(required_exercises: list, content: str) -> list:
        """Detecta los ejercicios faltantes basándose en los encabezados presentes en el contenido."""
        missing = [exercise for exercise in required_exercises if exercise not in content]
        return missing

    @staticmethod
    def analyze_images_in_pdf(pdf_path: str, required_exercises: list) -> list:
        """Analiza imágenes dentro de un PDF para detectar si contienen ejercicios requeridos."""
        try:
            images = FileProcessor.extract_images_from_pdf(pdf_path)
            detected_exercises = []
            for img in images:
                text = FileProcessor.extract_text_from_image(img)
                detected_exercises.extend([ex for ex in required_exercises if ex in text])
            return list(set(required_exercises) - set(detected_exercises))
        except Exception as e:
            logging.error(f"Error analizando imágenes en PDF {pdf_path}: {e}")
            return required_exercises
