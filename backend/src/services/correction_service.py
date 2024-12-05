import json
import logging
from typing import Dict, Any, List

import ollama
from src.config.settings import config
from src.utils.file_handler import FileHandler
from src.models.correction import CorrectionResult

class CorrectionService:
    """Servicio principal para corrección de tareas"""
    
    @staticmethod
    def _build_prompt(criteria: Dict, assignment: str) -> str:
        """Construir prompt inteligente para Ollama"""
        return f"""
        Evalúa la siguiente tarea basándote en estos criterios:
        Criterios: {json.dumps(criteria)}

        Tarea del estudiante: {assignment}

        Instrucciones para la evaluación:
        1. Califica la tarea de 0 a 10
        2. Proporciona comentarios detallados
        3. Justifica cada punto de la calificación
        4. Sé específico y constructivo

        Formato de respuesta (JSON estricto):
        {{
            "grade": float (0-10),
            "comments": "Comentarios detallados",
            "strengths": ["Punto fuerte 1", ...],
            "areas_of_improvement": ["Área de mejora 1", ...]
        }}
        """

    @classmethod
    def correct_assignment(
        cls, 
        key_criteria: Dict, 
        assignment_content: str
    ) -> CorrectionResult:
        """
        Corrige una tarea utilizando Ollama
        
        Args:
            key_criteria (Dict): Criterios de evaluación
            assignment_content (str): Contenido de la tarea
        
        Returns:
            CorrectionResult: Resultado de la corrección
        """
        try:
            prompt = cls._build_prompt(key_criteria, assignment_content)
            
            response = ollama.chat(
                model=config.OLLAMA_MODEL, 
                messages=[{'role': 'user', 'content': prompt}]
            )
            
            # Parsear respuesta JSON
            result_dict = json.loads(response['message']['content'])
            
            return CorrectionResult(
                grade=result_dict['grade'],
                comments=result_dict['comments'],
                strengths=result_dict.get('strengths', []),
                areas_of_improvement=result_dict.get('areas_of_improvement', [])
            )
        
        except Exception as e:
            logging.error(f"Error en corrección: {e}")
            return CorrectionResult(
                grade=0, 
                comments="Error en la evaluación automática"
            )

    @classmethod
    def batch_correction(
        cls, 
        key_criteria: Dict, 
        assignments: List[str]
    ) -> List[CorrectionResult]:
        """
        Corrige múltiples tareas en lote
        
        Args:
            key_criteria (Dict): Criterios de evaluación
            assignments (List[str]): Lista de contenidos de tareas
        
        Returns:
            List[CorrectionResult]: Lista de resultados
        """
        return [
            cls.correct_assignment(key_criteria, assignment) 
            for assignment in assignments
        ]