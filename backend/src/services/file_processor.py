import json
import re
from typing import Dict, List, Any, Optional
from pathlib import Path
import PyPDF2
import docx
from docx import Document
import logging

logger = logging.getLogger(__name__)

class FileProcessor:
    """Servicio para procesar archivos PDF y Word y extraer contenido estructurado"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.doc']
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Procesa un archivo y extrae su contenido estructurado
        
        Args:
            file_path: Ruta al archivo a procesar
            
        Returns:
            Dict con el contenido estructurado
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        if file_path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Formato no soportado: {file_path.suffix}")
        
        try:
            if file_path.suffix.lower() == '.pdf':
                return self._process_pdf(file_path)
            elif file_path.suffix.lower() in ['.docx', '.doc']:
                return self._process_docx(file_path)
        except Exception as e:
            logger.error(f"Error procesando archivo {file_path}: {str(e)}")
            raise
    
    def _process_pdf(self, file_path: Path) -> Dict[str, Any]:
        """Procesa un archivo PDF"""
        content = ""
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                content += f"\n--- Página {page_num + 1} ---\n"
                content += page_text
        
        return self._extract_structured_content(content, str(file_path))
    
    def _process_docx(self, file_path: Path) -> Dict[str, Any]:
        """Procesa un archivo Word"""
        doc = Document(file_path)
        content = ""
        
        for paragraph in doc.paragraphs:
            content += paragraph.text + "\n"
        
        return self._extract_structured_content(content, str(file_path))
    
    def _extract_structured_content(self, content: str, file_path: str) -> Dict[str, Any]:
        """
        Extrae contenido estructurado del texto
        
        Args:
            content: Contenido de texto del archivo
            file_path: Ruta del archivo original
            
        Returns:
            Dict con la estructura extraída
        """
        # Limpiar el contenido
        content = self._clean_content(content)
        
        # Extraer título
        title = self._extract_title(content)
        
        # Extraer instrucciones generales
        instructions = self._extract_instructions(content)
        
        # Extraer ejercicios
        exercises = self._extract_exercises(content)
        
        # Calcular puntos totales
        total_points = sum(exercise.get('points', 0) for exercise in exercises)
        
        return {
            "title": title,
            "instructions": instructions,
            "exercises": exercises,
            "total_points": total_points,
            "source_file": file_path,
            "extraction_metadata": {
                "extracted_at": None,  # Se llenará en el servicio
                "content_length": len(content),
                "exercise_count": len(exercises)
            }
        }
    
    def _clean_content(self, content: str) -> str:
        """Limpia el contenido del texto"""
        # Remover caracteres especiales y normalizar espacios
        content = re.sub(r'\s+', ' ', content)
        content = re.sub(r'[^\w\s\.\,\;\:\!\?\(\)\[\]\-\+\=\<\>\/]', '', content)
        return content.strip()
    
    def _extract_title(self, content: str) -> str:
        """Extrae el título del contenido"""
        lines = content.split('\n')
        
        # Buscar líneas que parezcan títulos (cortas, en mayúsculas, etc.)
        for line in lines[:10]:  # Buscar en las primeras 10 líneas
            line = line.strip()
            if len(line) > 5 and len(line) < 100:
                # Si la línea está en mayúsculas o tiene características de título
                if line.isupper() or any(keyword in line.lower() for keyword in 
                    ['ejercicio', 'actividad', 'tarea', 'práctica', 'examen']):
                    return line
        
        # Si no se encuentra título específico, usar las primeras palabras
        first_line = lines[0].strip() if lines else "Actividad sin título"
        return first_line[:50] + "..." if len(first_line) > 50 else first_line
    
    def _extract_instructions(self, content: str) -> str:
        """Extrae las instrucciones generales"""
        # Buscar patrones de instrucciones
        instruction_patterns = [
            r'instrucciones?[:\s]*(.*?)(?=\d+\.|ejercicio|pregunta)',
            r'consignas?[:\s]*(.*?)(?=\d+\.|ejercicio|pregunta)',
            r'indicaciones?[:\s]*(.*?)(?=\d+\.|ejercicio|pregunta)'
        ]
        
        for pattern in instruction_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                instructions = match.group(1).strip()
                if len(instructions) > 10:  # Solo si tiene contenido sustancial
                    return instructions[:500]  # Limitar longitud
        
        return ""
    
    def _extract_exercises(self, content: str) -> List[Dict[str, Any]]:
        """Extrae los ejercicios del contenido"""
        exercises = []
        
        # Patrones para identificar ejercicios
        exercise_patterns = [
            r'(\d+)\.\s*(.*?)(?=\d+\.|$)',  # 1. Enunciado...
            r'ejercicio\s*(\d+)[:\s]*(.*?)(?=ejercicio\s*\d+|$)',  # Ejercicio 1: ...
            r'pregunta\s*(\d+)[:\s]*(.*?)(?=pregunta\s*\d+|$)'  # Pregunta 1: ...
        ]
        
        for pattern in exercise_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)
            
            for match in matches:
                exercise_num = int(match.group(1))
                statement = match.group(2).strip()
                
                if len(statement) > 10:  # Solo ejercicios con contenido sustancial
                    # Intentar extraer puntos del enunciado
                    points = self._extract_points_from_statement(statement)
                    
                    # Determinar tipo de ejercicio
                    exercise_type = self._determine_exercise_type(statement)
                    
                    exercises.append({
                        "number": exercise_num,
                        "statement": statement[:1000],  # Limitar longitud
                        "type": exercise_type,
                        "points": points
                    })
        
        # Si no se encontraron ejercicios con patrones, intentar dividir por números
        if not exercises:
            exercises = self._extract_exercises_fallback(content)
        
        return exercises
    
    def _extract_points_from_statement(self, statement: str) -> int:
        """Extrae los puntos de un enunciado"""
        # Buscar patrones de puntos
        point_patterns = [
            r'(\d+)\s*puntos?',
            r'puntos?[:\s]*(\d+)',
            r'\((\d+)\s*p\)',
            r'\[(\d+)\s*p\]'
        ]
        
        for pattern in point_patterns:
            match = re.search(pattern, statement, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return 10  # Puntos por defecto
    
    def _determine_exercise_type(self, statement: str) -> str:
        """Determina el tipo de ejercicio basado en el enunciado"""
        statement_lower = statement.lower()
        
        if any(word in statement_lower for word in ['calcular', 'resolver', 'hallar', 'encontrar']):
            return 'calculation'
        elif any(word in statement_lower for word in ['explicar', 'describir', 'analizar', 'comentar']):
            return 'open_question'
        elif any(word in statement_lower for word in ['verdadero', 'falso', 'v/f']):
            return 'true_false'
        elif any(word in statement_lower for word in ['seleccionar', 'elegir', 'marcar']):
            return 'multiple_choice'
        elif any(word in statement_lower for word in ['completar', 'llenar', 'rellenar']):
            return 'fill_blank'
        else:
            return 'mixed'
    
    def _extract_exercises_fallback(self, content: str) -> List[Dict[str, Any]]:
        """Método alternativo para extraer ejercicios si los patrones fallan"""
        exercises = []
        lines = content.split('\n')
        
        current_exercise = None
        exercise_text = ""
        
        for line in lines:
            line = line.strip()
            
            # Buscar líneas que empiecen con número
            if re.match(r'^\d+\.?\s+', line):
                # Guardar ejercicio anterior si existe
                if current_exercise and len(exercise_text) > 10:
                    exercises.append({
                        "number": current_exercise,
                        "statement": exercise_text[:1000],
                        "type": "mixed",
                        "points": 10
                    })
                
                # Iniciar nuevo ejercicio
                match = re.match(r'^(\d+)\.?\s+(.*)', line)
                if match:
                    current_exercise = int(match.group(1))
                    exercise_text = match.group(2)
            elif current_exercise and line:
                exercise_text += " " + line
        
        # Agregar último ejercicio
        if current_exercise and len(exercise_text) > 10:
            exercises.append({
                "number": current_exercise,
                "statement": exercise_text[:1000],
                "type": "mixed",
                "points": 10
            })
        
        return exercises
