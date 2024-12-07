import json
import logging
import os
import sys
import re
import ollama

from typing import Dict, Any, List, Optional
from src.config.settings import config
from src.utils.file_handler import FileHandler
from src.models.correction import CorrectionResult
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache

# Configuración del path para que src sea reconocible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

executor = ProcessPoolExecutor(max_workers=os.cpu_count())

class CorrectionService:
    """Servicio principal para corrección de tareas"""
    @staticmethod
    def preprocess_text(text: str) -> str:
        """
        Preprocesar texto eliminando caracteres redundantes y truncando si es necesario.
        
        :param text: Texto original
        :return: Texto preprocesado
        """
        text = text.strip().replace("\n", " ").replace("\t", " ")
        return text[:1000] + "..." if len(text) > 1000 else text
    
    @staticmethod
    def _normalize_response(response_content: str) -> CorrectionResult:
        """
        Normaliza la respuesta de Ollama para asegurar el formato consistente.

        :param response_content: Respuesta como string.
        :return: CorrectionResult estandarizado.
        """
        try:
            # Intentar procesar como JSON válido
            response_json = json.loads(response_content)
            return CorrectionResult(
                grade=response_json.get("grade", 0.0),
                comments=response_json.get("comments", "Sin comentarios."),
                strengths=response_json.get("strengths", []),
                areas_of_improvement=response_json.get("areas_of_improvement", []),
            )
        except json.JSONDecodeError:
            logging.warning("Respuesta no es un JSON válido. Intentando analizar contenido como texto.")

        # Si JSON falla, intentar extraer contenido estructurado con regex
        try:
            grade_match = re.search(r'"?grade"?\s*:\s*(\d+(\.\d+)?)', response_content)
            comments_match = re.search(r'"?comments"?\s*:\s*"(.*?)"', response_content, re.DOTALL)
            strengths_match = re.search(r'"?strengths"?\s*:\s*\[(.*?)\]', response_content, re.DOTALL)
            improvements_match = re.search(r'"?areas_of_improvement"?\s*:\s*\[(.*?)\]', response_content, re.DOTALL)

            grade = float(grade_match.group(1)) if grade_match else 0.0
            comments = comments_match.group(1).strip() if comments_match else "Sin comentarios."
            strengths = json.loads(f"[{strengths_match.group(1)}]") if strengths_match else []
            areas_of_improvement = json.loads(f"[{improvements_match.group(1)}]") if improvements_match else []

            return CorrectionResult(
                grade=grade,
                comments=comments,
                strengths=strengths,
                areas_of_improvement=areas_of_improvement,
            )
        except Exception as e:
            logging.error(f"Error al analizar respuesta como texto estructurado: {e}")
            return CorrectionResult.default_error_result("Error en la evaluación automática")

    @staticmethod
    def _extract_json_content(response_content: str) -> str:
        """
        Extraer el contenido JSON válido de la respuesta.

        :param response_content: Respuesta como string.
        :return: JSON como string.
        """
        try:
            # Buscar bloques de JSON en el contenido
            match = re.search(r"\{.*\}", response_content, re.DOTALL)
            if match:
                return match.group(0)
            raise ValueError("No se encontró un bloque JSON válido en la respuesta.")
        except Exception as e:
            logging.error(f"Error al extraer JSON: {e}")
            raise

    @staticmethod
    def _build_prompt(criteria: Optional[Dict], assignment: str, language: str) -> str:
        """
        Construir el prompt para el modelo.

        :param criteria: Criterios clave.
        :param assignment: Contenido de la tarea.
        :param language: Idioma de respuesta.
        :return: Prompt.
        """
        if criteria:
            return f"""
            Evalúa la siguiente tarea basándote en estos criterios:
            Criterios: {json.dumps(criteria)}

            Tarea del estudiante: {assignment}

            Instrucciones para la evaluación:
            1. Califica la tarea de 0 a 10.
            2. Proporciona comentarios detallados.
            3. Identifica puntos fuertes y áreas de mejora específicos.
            4. Asegúrate de devolver la respuesta estrictamente en el formato JSON proporcionado.

            Idioma de la respuesta: {language}

            Formato de respuesta (JSON estricto):
            {{
                "grade": float (0-10),
                "comments": "Comentarios detallados",
                "strengths": ["Punto fuerte 1", ...],
                "areas_of_improvement": ["Área de mejora 1", ...]
            }}
            """
        
        return f"""
        Evalúa la siguiente tarea:
        Tarea del estudiante: {assignment}

        Instrucciones para la evaluación:
        1. Califica la tarea de 0 a 10.
        2. Proporciona comentarios detallados.
        3. Identifica puntos fuertes y áreas de mejora específicos.
        4. Asegúrate de devolver la respuesta estrictamente en el formato JSON proporcionado.

        Idioma de la respuesta: {language}

        Formato de respuesta (JSON estricto):
        {{
            "grade": float (0-10),
            "comments": "Comentarios detallados",
            "strengths": ["Punto fuerte 1", ...],
            "areas_of_improvement": ["Área de mejora 1", ...]
        }}
        """
    
    @staticmethod
    @lru_cache(maxsize=128)
    def cached_correction(criteria_hash, assignment_hash, language="es") -> CorrectionResult:
        """
        Corrección con caché para evitar evaluaciones repetidas.
        
        :param criteria_hash: Hash de los criterios clave
        :param assignment_hash: Hash de la tarea
        :param language: Idioma de la respuesta
        :return: Resultado de la corrección
        """
        return CorrectionService.correct_assignment(criteria_hash, assignment_hash, language)

    @classmethod
    def correct_assignment(
        cls, 
        key_criteria: Optional[Dict], 
        assignment_content: str,
        language: str = "español"
    ) -> CorrectionResult:
        """
        Corrige una tarea utilizando Ollama
        
        Args:
            key_criteria (Dict): Criterios de evaluación
            assignment_content (str): Contenido de la tarea
            language (str): Idioma de la respuesta
        
        Returns:
            CorrectionResult: Resultado de la corrección
        """
        try:
            # Preprocesar texto y construir prompt
            assignment_content = cls.preprocess_text(assignment_content)
            prompt = cls._build_prompt(key_criteria, assignment_content, language)

            # Llamar al modelo
            response = ollama.chat(
                model=config.OLLAMA_MODEL,
                messages=[{'role': 'user', 'content': prompt}]
            )

            # Procesar la respuesta del modelo
            response_content = response.get('message', {}).get('content', '').strip()
            logging.debug(f"Respuesta de Ollama: {response_content}")

            return cls._normalize_response(response_content)

        except Exception as e:
            logging.error(f"Error en corrección: {e}", exc_info=True)
            return CorrectionResult.default_error_result("Error en la evaluación automática")
        
    @staticmethod
    def _parse_with_regex(response_content: str) -> CorrectionResult:
        """
        Analiza la respuesta de Ollama utilizando expresiones regulares.

        :param response_content: Respuesta como string.
        :return: CorrectionResult.
        """
        try:
            grade_match = re.search(r"\"grade\":\s*(\d+(\.\d+)?)", response_content)
            comments_match = re.search(r"\"comments\":\s*\"(.*?)\"", response_content, re.DOTALL)
            strengths_match = re.search(r"\"strengths\":\s*\[(.*?)\]", response_content, re.DOTALL)
            improvements_match = re.search(r"\"areas_of_improvement\":\s*\[(.*?)\]", response_content, re.DOTALL)

            grade = float(grade_match.group(1)) if grade_match else 0.0
            comments = comments_match.group(1).strip() if comments_match else "Sin comentarios."
            strengths = [s.strip().strip('"') for s in strengths_match.group(1).split(",")] if strengths_match else []
            areas_of_improvement = [
                s.strip().strip('"') for s in improvements_match.group(1).split(",")
            ] if improvements_match else []

            return CorrectionResult(
                grade=grade,
                comments=comments,
                strengths=strengths,
                areas_of_improvement=areas_of_improvement,
            )
        except Exception as e:
            logging.error(f"Error al analizar con regex: {e}", exc_info=True)
            return CorrectionResult(
                grade=0.0,
                comments="Error en la evaluación automática",
            )

    @classmethod
    def batch_correction(
        cls, 
        key_criteria: Optional[Dict], 
        assignments: List[str],
        language: str = "español"
    ) -> List[CorrectionResult]:
        """
        Corrige múltiples tareas en lote
        
        Args:
            key_criteria (Optional[Dict]): Criterios de evaluación
            assignments (List[str]): Lista de contenidos de tareas
            language (str): Idioma de la respuesta
        
        Returns:
            List[CorrectionResult]: Lista de resultados
        """
        future_results = [
            executor.submit(cls.correct_assignment, key_criteria, assignment, language) 
            for assignment in assignments
        ]
        return [future.result() for future in future_results]