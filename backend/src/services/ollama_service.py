import ollama
import logging
from typing import Dict, Any, Optional

class OllamaService:
    def __init__(self, 
                 model: str = 'llama2', 
                 logger: Optional[logging.Logger] = None):
        """
        Inicializar servicio de Ollama
        
        :param model: Modelo de lenguaje a utilizar
        :param logger: Logger para registrar eventos
        """
        self.model = model
        self.logger = logger or logging.getLogger(__name__)

    def generate_prompt(self, 
                        task_content: str, 
                        evaluation_criteria: Dict[str, str]) -> str:
        """
        Generar un prompt para evaluación de tarea
        
        :param task_content: Contenido de la tarea a evaluar
        :param evaluation_criteria: Criterios de evaluación
        :return: Prompt generado
        """
        criteria_str = "\n".join([
            f"- {key.capitalize()}: {value}" 
            for key, value in evaluation_criteria.items()
        ])

        prompt = f"""
        Evalúa la siguiente tarea basándote en los siguientes criterios:
        
        Criterios de Evaluación:
        {criteria_str}

        Contenido de la Tarea:
        {task_content}

        Instrucciones:
        1. Califica la tarea de 0 a 10
        2. Proporciona comentarios detallados
        3. Explica tu calificación según los criterios

        Formato de Respuesta:
        - Nota: [Calificación de 0 a 10]
        - Comentarios: [Explicación detallada]
        """
        return prompt

    def evaluate_task(self, 
                      task_content: str, 
                      evaluation_criteria: Dict[str, str]) -> Dict[str, Any]:
        """
        Evaluar una tarea utilizando Ollama
        
        :param task_content: Contenido de la tarea
        :param evaluation_criteria: Criterios de evaluación
        :return: Diccionario con nota y comentarios
        """
        try:
            # Generar prompt
            prompt = self.generate_prompt(task_content, evaluation_criteria)

            # Llamada a Ollama
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}]
            )

            # Procesar respuesta
            result_text = response['message']['content']
            
            # Extraer nota y comentarios (implementación básica)
            nota = float(result_text.split('Nota: ')[1].split('\n')[0])
            comentarios = result_text.split('Comentarios: ')[1]

            self.logger.info(f"Tarea evaluada. Nota: {nota}")

            return {
                'nota': nota,
                'comentarios': comentarios
            }

        except Exception as e:
            self.logger.error(f"Error en evaluación de tarea: {e}")
            raise

    def validate_model_availability(self) -> bool:
        """
        Verificar disponibilidad del modelo
        
        :return: True si el modelo está disponible, False en caso contrario
        """
        try:
            # Intentar una consulta simple
            ollama.chat(
                model=self.model, 
                messages=[{'role': 'user', 'content': 'Hola'}]
            )
            self.logger.info(f"Modelo {self.model} disponible")
            return True
        except Exception as e:
            self.logger.error(f"Modelo {self.model} no disponible: {e}")
            return False