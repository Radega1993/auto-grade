import pytest
import os
import sys

# Configuración del path para que src sea reconocible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.services.correction_service import CorrectionService
from src.models.correction import CorrectionResult

@pytest.fixture
def key_criteria():
    return {
        "clarity": "La tarea debe ser clara y fácil de entender.",
        "depth": "La tarea debe mostrar una buena profundidad de conocimientos.",
        "structure": "La tarea debe tener una estructura lógica y organizada."
    }

@pytest.fixture
def assignment_content():
    return "Esta es una tarea de muestra que necesita ser evaluada."

def test_correct_assignment(key_criteria, assignment_content):
    result = CorrectionService.correct_assignment(key_criteria, assignment_content)
    assert isinstance(result, CorrectionResult)
    assert result.grade >= 0 and result.grade <= 10
    assert isinstance(result.comments, str)

def test_batch_correction(key_criteria):
    assignments = [
        "Tarea de muestra 1",
        "Tarea de muestra 2",
        "Tarea de muestra 3"
    ]
    results = CorrectionService.batch_correction(key_criteria, assignments)
    assert len(results) == len(assignments)
    for result in results:
        assert isinstance(result, CorrectionResult)
        assert result.grade >= 0 and result.grade <= 10
        assert isinstance(result.comments, str)
