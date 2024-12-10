import logging
import os
import json
import re
from typing import Dict, Any, List, Optional
from concurrent.futures import ProcessPoolExecutor

from src.models.correction import CorrectionResult
from src.services.file_processor import FileProcessor
from src.models.model_strategy import OllamaModelStrategy, OpenAIModelStrategy
from src.utils.analysis import Analysis

class CorrectionService:
    """Servicio principal para corrección de tareas"""

    def __init__(self, model_type: str = "ollama"):
        """
        Inicializa el servicio con la estrategia de modelo apropiada.

        :param model_type: Tipo de modelo a utilizar ('ollama' o 'openai').
        """
        if model_type == "openai":
            self.strategy = OpenAIModelStrategy()
        elif model_type == "ollama":
            self.strategy = OllamaModelStrategy()
        else:
            logging.error(f"Modelo desconocido: {model_type}. Usando Ollama por defecto.")
            self.strategy = OllamaModelStrategy()

    def validate_exercises(self, required_exercises: List[str], content: str) -> List[str]:
        """
        Valida si los ejercicios requeridos están presentes en el contenido.
        
        Args:
            required_exercises (List[str]): Lista de ejercicios requeridos.
            content (str): Contenido de la tarea.
            
        Returns:
            List[str]: Ejercicios faltantes.
        """
        missing_exercises = [exercise for exercise in required_exercises if exercise.lower() not in content.lower()]
        return missing_exercises

    @staticmethod
    def build_prompt(criteria: Optional[Dict], assignment: str, language: str) -> str:
        """
        Construir el prompt para el modelo.

        :param criteria: Criterios clave.
        :param assignment: Contenido de la tarea.
        :param language: Idioma de respuesta.
        :return: Prompt.
        """
        if criteria:
            return f"""
            Se te proporciona una tarea académica ya completada por un estudiante. Tu objetivo es evaluarla 
            técnicamente basándote en los siguientes criterios. No necesitas crear respuestas ni completar 
            ejercicios, solo evaluar el contenido que se te da.

            Criterios: {json.dumps(criteria)}

            Tarea del estudiante: {assignment}

            Instrucciones para la evaluación:
            1. Califica la tarea de 0 a 10 basándote exclusivamente en la calidad técnica de las respuestas proporcionadas y sé crítico.
            2. Proporciona comentarios detallados justificando la calificación asignada.
            3. Identifica puntos fuertes y áreas de mejora específicos.
            4. Responde estrictamente en el formato JSON proporcionado.

            Idioma de la respuesta: {language}

            Formato de respuesta:
            {{
                "grade": float (0-10),
                "comments": "Comentarios detallados",
                "strengths": ["Punto fuerte 1", ...],
                "areas_of_improvement": ["Área de mejora 1", ...]
            }}
            """
        return f"""
        Se te proporciona una tarea académica ya completada por un estudiante. Tu objetivo es evaluarla 
        técnicamente. No necesitas crear respuestas ni completar ejercicios, solo evaluar el contenido que se te da.

        Tarea del estudiante: {assignment}

        Instrucciones para la evaluación:
        1. Califica la tarea de 0 a 10 basándote exclusivamente en la calidad técnica de las respuestas proporcionadas.
        2. Proporciona comentarios detallados justificando la calificación asignada.
        3. Identifica puntos fuertes y áreas de mejora específicos.
        4. Responde estrictamente en el formato JSON proporcionado.

        Idioma de la respuesta: {language}

        Formato de respuesta:
        {{
            "grade": float (0-10),
            "comments": "Comentarios detallados",
            "strengths": ["Punto fuerte 1", ...],
            "areas_of_improvement": ["Área de mejora 1", ...]
        }}
        """
    
    def detect_ai_content(self, assignment_content: str) -> float:
        """
        Detecta el porcentaje de contenido generado con inteligencia artificial.

        Args:
            assignment_content (str): Contenido de la tarea.

        Returns:
            float: Porcentaje estimado de contenido generado con IA.
        """
        prompt = f"""
        Analiza el siguiente texto y estima qué porcentaje parece haber sido generado con inteligencia artificial. Responde estrictamente en el siguiente formato JSON:
        {{
            "ai_generated_percentage": float (0-100)
        }}

        Texto: {assignment_content}
        """
        try:
            response = self.strategy.evaluate(prompt)
            return response.get("ai_generated_percentage", 0.0)
        except Exception as e:
            logging.error(f"Error detectando contenido generado con IA: {e}")
            return 0.0
    
    def correct_assignment_with_ai_detection(self, key_criteria: Optional[Dict], assignment_content: str, language: str = "español") -> Dict[str, Any]:
        """
        Corrige una tarea y detecta contenido generado con IA.

        Args:
            key_criteria (Dict): Criterios de evaluación.
            assignment_content (str): Contenido de la tarea.
            language (str): Idioma de la respuesta.

        Returns:
            Dict[str, Any]: Resultado de la corrección incluyendo porcentaje de IA.
        """
        correction_result = self.correct_assignment(key_criteria, assignment_content, language)
        ai_percentage = Analysis.detect_ai_content(assignment_content, self.strategy)
        correction_dict = correction_result.to_dict()
        correction_dict["ai_generated_percentage"] = round(ai_percentage, 2)
        return correction_dict

    def correct_assignment_with_validation(self, key_criteria: Optional[Dict], assignment_content: str, required_exercises: List[str], language: str = "español") -> Dict[str, Any]:
        """
        Corrige una tarea validando ejercicios, analizando IA, y detectando ejercicios faltantes.

        Args:
            key_criteria (Dict): Criterios de evaluación.
            assignment_content (str): Contenido de la tarea.
            required_exercises (List[str]): Ejercicios requeridos.
            language (str): Idioma de la respuesta.

        Returns:
            Dict[str, Any]: Resultado de la corrección con ejercicios faltantes.
        """
        missing_exercises = self.validate_exercises(required_exercises, assignment_content)
        correction_result = self.correct_assignment(key_criteria, assignment_content, language)
        ai_percentage = self.detect_ai_content(assignment_content)
        
        correction_dict = correction_result.to_dict()
        correction_dict["missing_exercises"] = missing_exercises
        correction_dict["ai_generated_percentage"] = round(ai_percentage, 2)
        return correction_dict

    def correct_assignment(self, key_criteria: Optional[Dict], assignment_content: str, language: str = "español") -> CorrectionResult:
        """
        Corrige una tarea utilizando la estrategia de modelo configurada.

        Args:
            key_criteria (Dict): Criterios de evaluación.
            assignment_content (str): Contenido de la tarea.
            language (str): Idioma de la respuesta.

        Returns:
            CorrectionResult: Resultado de la corrección.
        """
        if not assignment_content.strip():
            logging.error("El contenido de la tarea está vacío o no válido.")
            return CorrectionResult.default_error_result("El contenido de la tarea está vacío o no válido.")

        try:
            # Construir el prompt
            prompt = self.build_prompt(key_criteria, assignment_content, language)
            # Evaluar usando la estrategia configurada
            response = self.strategy.evaluate(prompt)

            # Procesar la respuesta
            if "error" in response:
                return CorrectionResult.default_error_result(response["error"])

            return CorrectionResult.from_response(response)
        except Exception as e:
            logging.error(f"Error en la corrección: {e}")
            return CorrectionResult.default_error_result("Error en la evaluación automática.")

    @staticmethod
    def process_task(args: Dict[str, Any]) -> CorrectionResult:
        """
        Método estático para procesar una tarea dentro de un pool de procesos.

        :param args: Diccionario con argumentos necesarios para la corrección.
        :return: CorrectionResult
        """
        try:
            service = CorrectionService(args["model_type"])
            return service.correct_assignment(
                key_criteria=args["key_criteria"],
                assignment_content=args["assignment_content"],
                language=args["language"],
            )
        except Exception as e:
            return CorrectionResult.default_error_result("Error interno en process_task.")

    @classmethod
    def batch_correction(cls, model_type: str, key_criteria: Optional[Dict], assignments: List[str], language: str = "español") -> List[CorrectionResult]:
        """
        Corrige múltiples tareas en paralelo.

        Args:
            model_type (str): Tipo de modelo ('ollama' o 'openai').
            key_criteria (Optional[Dict]): Criterios de evaluación.
            assignments (List[str]): Lista de contenidos de tareas.
            language (str): Idioma de la respuesta.

        Returns:
            List[CorrectionResult]: Lista de resultados.
        """
        tasks = [
            {
                "model_type": model_type,
                "key_criteria": key_criteria,
                "assignment_content": assignment,
                "language": language,
            }
            for assignment in assignments
        ]

        results = []
        with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
            # Crear tareas de corrección
            futures = [executor.submit(CorrectionService.process_task, task) for task in tasks]

            # Recopilar resultados
            for future in futures:
                try:
                    results.append(future.result())
                except Exception as e:
                    results.append(CorrectionResult.default_error_result("Error procesando la tarea."))

        return results
