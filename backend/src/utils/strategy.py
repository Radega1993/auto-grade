# backend/src/utils/strategy.py
from abc import ABC, abstractmethod
from typing import Dict

class BaseEvaluationStrategy(ABC):
    @abstractmethod
    def evaluate(self, content: str, criteria: Dict):
        pass

class OllamaEvaluationStrategy(BaseEvaluationStrategy):
    def evaluate(self, content: str, criteria: Dict):
        # Integración con Ollama
        pass

class OpenAIEvaluationStrategy(BaseEvaluationStrategy):
    def evaluate(self, content: str, criteria: Dict):
        # Integración con OpenAI ChatGPT
        pass