import ollama
import logging
import json
import re
import os

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from typing import Dict, Any
from abc import ABC, abstractmethod

class ModelStrategy(ABC):
    """Abstract base class for all model strategies."""
    @abstractmethod
    def evaluate(self, prompt: str) -> Dict[str, Any]:
        pass

class OllamaModelStrategy(ModelStrategy):
    def evaluate(self, prompt: str) -> Dict[str, Any]:
        try:
            response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])
            content = response.get("message", {}).get("content", "")
            return self._parse_response(content)
        except Exception as e:
            return {"error": "Failed to evaluate using Ollama."}

    def _parse_response(self, content: str) -> Dict[str, Any]:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logging.warning("Parsing response with regex fallback.")
            return self._parse_with_regex(content)

    def _parse_with_regex(self, content: str) -> Dict[str, Any]:
        try:
            grade_match = re.search(r'"grade":\s*(\d+(\.\d+)?)', content)
            comments_match = re.search(r'"comments":\s*"(.*?)"', content, re.DOTALL)
            strengths_match = re.search(r'"strengths":\s*\[(.*?)\]', content, re.DOTALL)
            improvements_match = re.search(r'"areas_of_improvement":\s*\[(.*?)\]', content, re.DOTALL)

            # Verificar si las coincidencias existen antes de acceder a group()
            grade = float(grade_match.group(1)) if grade_match else 0.0
            comments = comments_match.group(1) if comments_match else "No se proporcionaron comentarios."
            strengths = json.loads(f"[{strengths_match.group(1)}]") if strengths_match else []
            areas_of_improvement = json.loads(f"[{improvements_match.group(1)}]") if improvements_match else []

            return {
                "grade": grade,
                "comments": comments,
                "strengths": strengths,
                "areas_of_improvement": areas_of_improvement,
            }
        except Exception as e:
            return {"grade": 0.0, "comments": "Error parsing response."}
        
class OpenAIModelStrategy(ModelStrategy):
    def __init__(self):
        """Inicializa la estrategia de OpenAI."""
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("Falta la clave de API de OpenAI en las variables de entorno.")
        self.llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-4",
            openai_api_key=openai_api_key
        )

    def evaluate(self, prompt: str) -> Dict[str, Any]:
        try:
            response = self.llm.predict(prompt)
            return json.loads(response)
        except json.JSONDecodeError:
            return {"error": "Respuesta JSON inválida de OpenAI."}
        except Exception as e:
            return {"error": "Error en la evaluación con OpenAI."}