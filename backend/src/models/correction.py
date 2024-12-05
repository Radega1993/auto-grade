from dataclasses import dataclass, asdict
from typing import List, Optional

@dataclass
class CorrectionResult:
    """
    Modelo de datos para resultados de corrección
    """
    grade: float
    comments: str
    strengths: List[str] = None
    areas_of_improvement: List[str] = None
    
    def __post_init__(self):
        """
        Inicialización posterior para manejar valores por defecto
        """
        # Asegurar que las listas sean inicializadas si son None
        if self.strengths is None:
            self.strengths = []
        if self.areas_of_improvement is None:
            self.areas_of_improvement = []
        
        # Validar rango de calificación
        self.grade = max(0.0, min(10.0, self.grade))
    
    def to_dict(self) -> dict:
        """
        Convertir el resultado a un diccionario
        
        :return: Diccionario con los datos de corrección
        """
        return {
            'grade': round(self.grade, 2),
            'comments': self.comments,
            'strengths': self.strengths,
            'areas_of_improvement': self.areas_of_improvement
        }
    
    @classmethod
    def default_error_result(cls, error_message: str = "Error en evaluación"):
        """
        Crear un resultado de corrección por defecto en caso de error
        
        :param error_message: Mensaje de error personalizado
        :return: Instancia de CorrectionResult con calificación 0
        """
        return cls(
            grade=0.0,
            comments=error_message
        )
