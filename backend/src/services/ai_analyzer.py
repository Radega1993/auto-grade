import json
import logging
from typing import Dict, List, Any, Optional
import openai
from datetime import datetime

logger = logging.getLogger(__name__)

class AIAnalyzer:
    """Servicio para analizar actividades con IA y generar soluciones y rúbricas"""
    
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
    
    def analyze_assignment(self, extracted_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analiza una actividad y genera soluciones y rúbrica
        
        Args:
            extracted_content: Contenido extraído del archivo
            
        Returns:
            Dict con soluciones y rúbrica generadas por IA
        """
        try:
            # Crear prompt para la IA
            prompt = self._create_analysis_prompt(extracted_content)
            
            # Llamar a la IA
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=4000
            )
            
            # Procesar respuesta
            ai_response = response.choices[0].message.content
            logger.info(f"Respuesta de IA recibida: {ai_response[:200]}...")
            
            analysis_result = self._parse_ai_response(ai_response)
            
            # Agregar metadatos
            analysis_result["ai_metadata"] = {
                "model_used": self.model,
                "analyzed_at": datetime.utcnow().isoformat(),
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error en análisis de IA: {str(e)}")
            raise
    
    def _get_system_prompt(self) -> str:
        """Obtiene el prompt del sistema para la IA"""
        return """Eres un experto en educación y evaluación académica. Tu tarea es analizar actividades educativas y generar:

1. SOLUCIONES DETALLADAS: Para cada ejercicio, proporciona la respuesta esperada, pasos de solución y explicaciones claras.

2. RÚBRICA DE EVALUACIÓN: Crea criterios de evaluación específicos, medibles y justos para cada ejercicio.

IMPORTANTE:
- Responde ÚNICAMENTE en formato JSON válido
- No incluyas texto adicional fuera del JSON
- Sé preciso y educativo en tus respuestas
- Considera diferentes niveles de desempeño
- Incluye criterios específicos para cada tipo de ejercicio
- Mantén un enfoque pedagógico constructivo

Formato de respuesta requerido:
{
  "solutions": [
    {
      "exercise_number": 1,
      "expected_answer": "respuesta esperada",
      "solution_steps": ["paso 1", "paso 2"],
      "explanation": "explicación detallada"
    }
  ],
  "rubric": {
    "criteria": [
      {
        "name": "Criterio 1",
        "description": "Descripción del criterio",
        "weight": 0.3,
        "levels": [
          {
            "name": "Excelente",
            "description": "Descripción del nivel",
            "points": 10
          }
        ]
      }
    ],
    "total_points": 100
  }
}"""
    
    def _create_analysis_prompt(self, content: Dict[str, Any]) -> str:
        """Crea el prompt específico para analizar la actividad"""
        prompt = f"""
Analiza la siguiente actividad educativa y genera soluciones detalladas y una rúbrica de evaluación.

TÍTULO: {content.get('title', 'Sin título')}

INSTRUCCIONES: {content.get('instructions', 'Sin instrucciones específicas')}

EJERCICIOS:
"""
        
        for exercise in content.get('exercises', []):
            prompt += f"""
Ejercicio {exercise.get('number', 'N/A')}: {exercise.get('statement', 'Sin enunciado')}
Puntos: {exercise.get('points', 0)}
"""
        
        prompt += f"""
PUNTOS TOTALES: {content.get('total_points', 0)}

Por favor, genera:
1. Soluciones detalladas para cada ejercicio
2. Una rúbrica de evaluación completa

Responde ÚNICAMENTE con el JSON en el formato especificado.
"""
        
        return prompt
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parsea la respuesta de la IA y la convierte a JSON"""
        try:
            # Limpiar la respuesta
            response = response.strip()
            
            # Buscar el JSON en la respuesta
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            
            # Si la respuesta no es JSON válido, crear una respuesta por defecto
            try:
                result = json.loads(response)
            except json.JSONDecodeError:
                logger.warning("La respuesta de IA no es JSON válido, creando respuesta por defecto")
                result = self._create_default_response()
            
            # Validar estructura
            if not isinstance(result, dict):
                result = self._create_default_response()
            
            if 'solutions' not in result or 'rubric' not in result:
                result = self._create_default_response()
            
            # Validar y completar soluciones
            if not isinstance(result.get('solutions'), list):
                result['solutions'] = []
            
            # Validar y completar rúbrica
            if not isinstance(result.get('rubric'), dict):
                result['rubric'] = self._create_default_rubric()
            
            return result
            
        except Exception as e:
            logger.error(f"Error procesando respuesta de IA: {str(e)}")
            return self._create_default_response()
    
    def _create_default_response(self) -> Dict[str, Any]:
        """Crea una respuesta por defecto cuando la IA falla"""
        return {
            "solutions": [
                {
                    "exercise_number": 1,
                    "expected_answer": "Respuesta por defecto - requiere revisión manual",
                    "solution_steps": ["Paso 1: Revisar el ejercicio", "Paso 2: Proporcionar solución manual"],
                    "explanation": "Esta solución fue generada automáticamente debido a un error en el análisis de IA. Por favor, revise y edite manualmente."
                }
            ],
            "rubric": self._create_default_rubric()
        }
    
    def _create_default_rubric(self) -> Dict[str, Any]:
        """Crea una rúbrica por defecto"""
        return {
            "criteria": [
                {
                    "name": "Comprensión del ejercicio",
                    "description": "El estudiante demuestra comprensión del ejercicio planteado",
                    "weight": 0.4,
                    "levels": [
                        {
                            "name": "Excelente",
                            "description": "Comprensión completa y correcta",
                            "points": 10
                        },
                        {
                            "name": "Bueno",
                            "description": "Comprensión mayormente correcta",
                            "points": 7
                        },
                        {
                            "name": "Regular",
                            "description": "Comprensión parcial",
                            "points": 4
                        },
                        {
                            "name": "Insuficiente",
                            "description": "Comprensión limitada o incorrecta",
                            "points": 1
                        }
                    ]
                },
                {
                    "name": "Desarrollo de la solución",
                    "description": "El estudiante desarrolla correctamente la solución",
                    "weight": 0.6,
                    "levels": [
                        {
                            "name": "Excelente",
                            "description": "Solución completa y correcta",
                            "points": 10
                        },
                        {
                            "name": "Bueno",
                            "description": "Solución mayormente correcta",
                            "points": 7
                        },
                        {
                            "name": "Regular",
                            "description": "Solución parcialmente correcta",
                            "points": 4
                        },
                        {
                            "name": "Insuficiente",
                            "description": "Solución incorrecta o incompleta",
                            "points": 1
                        }
                    ]
                }
            ],
            "total_points": 100
        }
