import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from sqlalchemy import and_

from ..database.database import db
from ..database.models import Assignment, AssignmentStatus, User
from .file_processor import FileProcessor
from .ai_analyzer import AIAnalyzer
from ..config.settings import config

logger = logging.getLogger(__name__)

class AssignmentService:
    """Servicio para gestionar asignaciones"""
    
    def __init__(self):
        self.upload_folder = config.UPLOAD_FOLDER
        self.file_processor = FileProcessor()
        self.ai_analyzer = AIAnalyzer(config.OPENAI_API_KEY)
        
        # Crear directorio de uploads si no existe
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def create_assignment_from_file(self, file, title: str, description: str, teacher_id: str) -> Dict[str, Any]:
        """Crea una nueva asignación desde un archivo"""
        try:
            # Guardar archivo temporalmente
            temp_file_path = self._save_temp_file(file)
            
            try:
                # Procesar archivo
                logger.info(f"Procesando archivo: {temp_file_path}")
                extracted_content = self.file_processor.extract_content(temp_file_path)
                
                # Crear asignación en BD
                assignment = Assignment(
                    title=title,
                    description=description,
                    teacher_id=teacher_id,
                    extracted_content=extracted_content,
                    status=AssignmentStatus.UPLOADED,
                    total_points=extracted_content.get('total_points', 100.0)
                )
                
                db.session.add(assignment)
                db.session.commit()
                
                logger.info(f"Asignación creada: {assignment.id}")
                
                # Iniciar análisis de IA de forma asíncrona
                self._start_ai_analysis(assignment.id)
                
                return {
                    "id": str(assignment.id),
                    "title": assignment.title,
                    "status": assignment.status.value,
                    "message": "Asignación creada exitosamente. El análisis con IA está en proceso."
                }
                
            finally:
                # Limpiar archivo temporal
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                    
        except Exception as e:
            logger.error(f"Error creando asignación: {str(e)}")
            db.session.rollback()
            raise
    
    def get_assignment(self, assignment_id: str, teacher_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una asignación por ID"""
        try:
            assignment = db.session.query(Assignment).filter(
                Assignment.id == assignment_id,
                Assignment.teacher_id == teacher_id
            ).first()
            
            if not assignment:
                return None
            
            return self._assignment_to_dict(assignment)
            
        except Exception as e:
            logger.error(f"Error obteniendo asignación {assignment_id}: {str(e)}")
            raise
    
    def get_teacher_assignments(self, teacher_id: str) -> List[Dict[str, Any]]:
        """Obtiene todas las asignaciones de un profesor"""
        try:
            assignments = db.session.query(Assignment).filter(
                Assignment.teacher_id == teacher_id
            ).order_by(Assignment.created_at.desc()).all()
            
            return [self._assignment_to_dict(assignment) for assignment in assignments]
            
        except Exception as e:
            logger.error(f"Error obteniendo asignaciones del profesor {teacher_id}: {str(e)}")
            raise
    
    def update_assignment_solutions(self, assignment_id: str, teacher_id: str, solutions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Actualiza las soluciones de una asignación"""
        try:
            assignment = db.session.query(Assignment).filter(
                Assignment.id == assignment_id,
                Assignment.teacher_id == teacher_id
            ).first()
            
            if not assignment:
                return {"error": "Asignación no encontrada"}
            
            assignment.final_solutions = solutions
            assignment.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {"message": "Soluciones actualizadas exitosamente"}
            
        except Exception as e:
            logger.error(f"Error actualizando soluciones: {str(e)}")
            db.session.rollback()
            raise
    
    def update_assignment_rubric(self, assignment_id: str, teacher_id: str, rubric: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza la rúbrica de una asignación"""
        try:
            assignment = db.session.query(Assignment).filter(
                Assignment.id == assignment_id,
                Assignment.teacher_id == teacher_id
            ).first()
            
            if not assignment:
                return {"error": "Asignación no encontrada"}
            
            assignment.final_rubric = rubric
            assignment.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {"message": "Rúbrica actualizada exitosamente"}
            
        except Exception as e:
            logger.error(f"Error actualizando rúbrica: {str(e)}")
            db.session.rollback()
            raise
    
    def finalize_assignment(self, assignment_id: str, teacher_id: str) -> Dict[str, Any]:
        """Finaliza una asignación para uso en correcciones"""
        try:
            assignment = db.session.query(Assignment).filter(
                Assignment.id == assignment_id,
                Assignment.teacher_id == teacher_id
            ).first()
            
            if not assignment:
                return {"error": "Asignación no encontrada"}
            
            if assignment.status != AssignmentStatus.READY_FOR_EDITING:
                return {"error": "La asignación debe estar en estado 'ready_for_editing'"}
            
            assignment.status = AssignmentStatus.FINALIZED
            assignment.updated_at = datetime.utcnow()
            db.session.commit()
            
            return {"message": "Asignación finalizada exitosamente"}
            
        except Exception as e:
            logger.error(f"Error finalizando asignación: {str(e)}")
            db.session.rollback()
            raise
    
    def check_stuck_assignments(self) -> int:
        """Verifica y marca como error las asignaciones que llevan más de 1 hora procesando"""
        try:
            # Buscar asignaciones en procesamiento por más de 1 hora
            one_hour_ago = datetime.utcnow() - timedelta(hours=1)
            
            stuck_assignments = db.session.query(Assignment).filter(
                and_(
                    Assignment.status == AssignmentStatus.PROCESSING,
                    Assignment.updated_at < one_hour_ago
                )
            ).all()
            
            count = 0
            for assignment in stuck_assignments:
                logger.warning(f"Marcando asignación {assignment.id} como error por timeout")
                assignment.status = AssignmentStatus.ERROR
                assignment.updated_at = datetime.utcnow()
                count += 1
            
            if count > 0:
                db.session.commit()
                logger.info(f"Marcadas {count} asignaciones como error por timeout")
            
            return count
            
        except Exception as e:
            logger.error(f"Error verificando asignaciones bloqueadas: {str(e)}")
            db.session.rollback()
            return 0
    
    def _save_temp_file(self, file) -> str:
        """Guarda un archivo temporalmente"""
        filename = secure_filename(file.filename)
        temp_filename = f"temp_{os.urandom(16).hex()}_{filename}"
        temp_path = os.path.join(self.upload_folder, temp_filename)
        
        file.save(temp_path)
        return temp_path
    
    def _start_ai_analysis(self, assignment_id: str) -> None:
        """Inicia el análisis con IA de forma asíncrona"""
        try:
            # En una implementación real, esto se haría con una cola de tareas (Celery, RQ, etc.)
            # Por ahora, lo hacemos de forma síncrona
            self._process_ai_analysis(assignment_id)
            
        except Exception as e:
            logger.error(f"Error iniciando análisis de IA: {str(e)}")
            # Marcar asignación como error
            self._mark_assignment_error(assignment_id, str(e))
    
    def _process_ai_analysis(self, assignment_id: str) -> None:
        """Procesa el análisis con IA"""
        try:
            assignment = db.session.query(Assignment).filter(
                Assignment.id == assignment_id
            ).first()
            
            if not assignment:
                logger.error(f"Asignación {assignment_id} no encontrada para análisis")
                return
            
            # Actualizar estado a procesando
            assignment.status = AssignmentStatus.PROCESSING
            db.session.commit()
            
            # Analizar con IA
            logger.info(f"Iniciando análisis de IA para asignación {assignment_id}")
            ai_analysis = self.ai_analyzer.analyze_assignment(assignment.extracted_content)
            
            # Guardar análisis
            assignment.ai_analysis = ai_analysis
            assignment.final_solutions = ai_analysis.get('solutions', [])
            assignment.final_rubric = ai_analysis.get('rubric', {})
            assignment.status = AssignmentStatus.READY_FOR_EDITING
            assignment.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            logger.info(f"Análisis de IA completado para asignación {assignment_id}")
            
        except Exception as e:
            logger.error(f"Error en análisis de IA: {str(e)}")
            self._mark_assignment_error(assignment_id, str(e))
    
    def _mark_assignment_error(self, assignment_id: str, error_message: str) -> None:
        """Marca una asignación como error"""
        try:
            assignment = db.session.query(Assignment).filter(
                Assignment.id == assignment_id
            ).first()
            
            if assignment:
                assignment.status = AssignmentStatus.ERROR
                assignment.updated_at = datetime.utcnow()
                db.session.commit()
                
        except Exception as e:
            logger.error(f"Error marcando asignación como error: {str(e)}")
    
    def _assignment_to_dict(self, assignment: Assignment) -> Dict[str, Any]:
        """Convierte un objeto Assignment a diccionario"""
        return {
            "id": str(assignment.id),
            "title": assignment.title,
            "description": assignment.description,
            "status": assignment.status.value,
            "teacher_id": str(assignment.teacher_id),
            "extracted_content": assignment.extracted_content,
            "ai_analysis": assignment.ai_analysis,
            "final_solutions": assignment.final_solutions,
            "final_rubric": assignment.final_rubric,
            "created_at": assignment.created_at.isoformat() if assignment.created_at else None,
            "updated_at": assignment.updated_at.isoformat() if assignment.updated_at else None
        }
    
    def delete_assignment(self, assignment_id: str, teacher_id: str) -> Dict[str, Any]:
        """Elimina una asignación"""
        try:
            assignment = db.session.query(Assignment).filter(
                Assignment.id == assignment_id,
                Assignment.teacher_id == teacher_id
            ).first()
            
            if not assignment:
                return {"error": "Asignación no encontrada"}
            
            db.session.delete(assignment)
            db.session.commit()
            
            return {"message": "Asignación eliminada exitosamente"}
            
        except Exception as e:
            logger.error(f"Error eliminando asignación: {str(e)}")
            db.session.rollback()
            raise
    
    def generate_rubric_pdf(self, assignment_id: str, teacher_id: str) -> Dict[str, Any]:
        """Genera un PDF con la rúbrica de la asignación"""
        try:
            assignment = db.session.query(Assignment).filter(
                Assignment.id == assignment_id,
                Assignment.teacher_id == teacher_id
            ).first()
            
            if not assignment:
                return {"error": "Asignación no encontrada"}
            
            if not assignment.final_rubric:
                return {"error": "No hay rúbrica disponible para esta asignación"}
            
            # Generar PDF usando reportlab
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            from reportlab.lib.units import inch
            import io
            
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1  # Centrado
            )
            story.append(Paragraph(f"Rúbrica: {assignment.title}", title_style))
            story.append(Spacer(1, 12))
            
            # Información de la asignación
            info_style = ParagraphStyle(
                'Info',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=6
            )
            story.append(Paragraph(f"<b>Descripción:</b> {assignment.description or 'Sin descripción'}", info_style))
            story.append(Paragraph(f"<b>Puntos totales:</b> {assignment.total_points}", info_style))
            story.append(Spacer(1, 20))
            
            # Criterios
            rubric = assignment.final_rubric
            criteria = rubric.get('criteria', [])
            
            for i, criterion in enumerate(criteria, 1):
                # Título del criterio
                criterion_style = ParagraphStyle(
                    'CriterionTitle',
                    parent=styles['Heading2'],
                    fontSize=14,
                    spaceAfter=12,
                    textColor=colors.darkblue
                )
                story.append(Paragraph(f"Criterio {i}: {criterion.get('name', 'Sin nombre')}", criterion_style))
                
                # Descripción del criterio
                if criterion.get('description'):
                    story.append(Paragraph(f"<b>Descripción:</b> {criterion['description']}", styles['Normal']))
                    story.append(Spacer(1, 8))
                
                # Peso
                story.append(Paragraph(f"<b>Peso:</b> {criterion.get('weight', 0):.1%}", styles['Normal']))
                story.append(Spacer(1, 12))
                
                # Niveles de desempeño
                levels = criterion.get('performance_levels', [])
                if levels:
                    # Crear tabla de niveles
                    table_data = [['Nivel', 'Descripción', 'Puntos']]
                    for level in levels:
                        table_data.append([
                            level.get('name', 'Sin nombre'),
                            level.get('description', 'Sin descripción'),
                            str(level.get('points', 0))
                        ])
                    
                    table = Table(table_data, colWidths=[1.5*inch, 3*inch, 0.8*inch])
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    
                    story.append(table)
                
                story.append(Spacer(1, 20))
            
            # Construir PDF
            doc.build(story)
            buffer.seek(0)
            
            filename = f"rubrica_{assignment.title.replace(' ', '_')}.pdf"
            
            return {
                "pdf_content": buffer.getvalue(),
                "filename": filename
            }
            
        except Exception as e:
            logger.error(f"Error generando PDF de rúbrica: {str(e)}")
            raise
    
    def generate_solutions_pdf(self, assignment_id: str, teacher_id: str) -> Dict[str, Any]:
        """Genera un PDF con las soluciones de la asignación"""
        try:
            assignment = db.session.query(Assignment).filter(
                Assignment.id == assignment_id,
                Assignment.teacher_id == teacher_id
            ).first()
            
            if not assignment:
                return {"error": "Asignación no encontrada"}
            
            if not assignment.final_solutions:
                return {"error": "No hay soluciones disponibles para esta asignación"}
            
            # Generar PDF usando reportlab
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors
            from reportlab.lib.units import inch
            import io
            
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1  # Centrado
            )
            story.append(Paragraph(f"Soluciones: {assignment.title}", title_style))
            story.append(Spacer(1, 12))
            
            # Información de la asignación
            info_style = ParagraphStyle(
                'Info',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=6
            )
            story.append(Paragraph(f"<b>Descripción:</b> {assignment.description or 'Sin descripción'}", info_style))
            story.append(Paragraph(f"<b>Puntos totales:</b> {assignment.total_points}", info_style))
            story.append(Spacer(1, 20))
            
            # Soluciones
            solutions = assignment.final_solutions
            
            for i, solution in enumerate(solutions, 1):
                # Título del ejercicio
                exercise_style = ParagraphStyle(
                    'ExerciseTitle',
                    parent=styles['Heading2'],
                    fontSize=14,
                    spaceAfter=12,
                    textColor=colors.darkgreen
                )
                story.append(Paragraph(f"Ejercicio {i}", exercise_style))
                
                # Respuesta esperada
                if solution.get('expected_answer'):
                    story.append(Paragraph(f"<b>Respuesta esperada:</b>", styles['Normal']))
                    story.append(Paragraph(solution['expected_answer'], styles['Normal']))
                    story.append(Spacer(1, 8))
                
                # Pasos de solución
                steps = solution.get('solution_steps', [])
                if steps:
                    story.append(Paragraph(f"<b>Pasos de solución:</b>", styles['Normal']))
                    for j, step in enumerate(steps, 1):
                        if step.strip():  # Solo agregar pasos no vacíos
                            story.append(Paragraph(f"{j}. {step}", styles['Normal']))
                    story.append(Spacer(1, 8))
                
                # Explicación
                if solution.get('explanation'):
                    story.append(Paragraph(f"<b>Explicación:</b>", styles['Normal']))
                    story.append(Paragraph(solution['explanation'], styles['Normal']))
                    story.append(Spacer(1, 8))
                
                # Conceptos clave
                concepts = solution.get('key_concepts', [])
                if concepts:
                    concepts_text = ", ".join([c for c in concepts if c.strip()])
                    if concepts_text:
                        story.append(Paragraph(f"<b>Conceptos clave:</b> {concepts_text}", styles['Normal']))
                
                story.append(Spacer(1, 20))
            
            # Construir PDF
            doc.build(story)
            buffer.seek(0)
            
            filename = f"soluciones_{assignment.title.replace(' ', '_')}.pdf"
            
            return {
                "pdf_content": buffer.getvalue(),
                "filename": filename
            }
            
        except Exception as e:
            logger.error(f"Error generando PDF de soluciones: {str(e)}")
            raise
