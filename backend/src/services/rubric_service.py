"""
Servicio para gestión de rúbricas
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..database.database import db
from ..database.models import Rubric, User, UserRole

logger = logging.getLogger(__name__)

class RubricService:
    """Servicio para manejar rúbricas"""
    
    @staticmethod
    def create_rubric(teacher_id: str, rubric_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea una nueva rúbrica
        
        Args:
            teacher_id: ID del profesor
            rubric_data: Datos de la rúbrica
            
        Returns:
            Dict con información de la rúbrica creada
        """
        try:
            # Validar que el profesor existe
            teacher = db.session.query(User).filter(User.id == teacher_id).first()
            if not teacher:
                raise ValueError("Profesor no encontrado")
            
            # Validar estructura de criterios
            criteria = rubric_data.get('criteria', [])
            if not criteria:
                raise ValueError("La rúbrica debe tener al menos un criterio")
            
            # Validar que la suma de puntos sea correcta
            total_criteria_points = sum(criterion.get('points', 0) for criterion in criteria)
            if abs(total_criteria_points - rubric_data.get('total_points', 100)) > 0.01:
                raise ValueError("La suma de puntos de los criterios debe coincidir con el total")
            
            # Crear rúbrica
            new_rubric = Rubric(
                title=rubric_data['title'],
                description=rubric_data.get('description', ''),
                subject=rubric_data.get('subject', ''),
                grade_level=rubric_data.get('grade_level', ''),
                total_points=rubric_data.get('total_points', 100.0),
                teacher_id=teacher_id,
                criteria=criteria,
                is_template=rubric_data.get('is_template', False),
                is_public=rubric_data.get('is_public', False)
            )
            
            db.session.add(new_rubric)
            db.session.commit()
            
            logger.info(f"Rúbrica creada: {new_rubric.title} por {teacher.email}")
            
            return {
                'id': str(new_rubric.id),
                'title': new_rubric.title,
                'description': new_rubric.description,
                'subject': new_rubric.subject,
                'grade_level': new_rubric.grade_level,
                'total_points': new_rubric.total_points,
                'criteria': new_rubric.criteria,
                'is_template': new_rubric.is_template,
                'is_public': new_rubric.is_public,
                'teacher_id': str(new_rubric.teacher_id),
                'created_at': new_rubric.created_at.isoformat() if new_rubric.created_at else None
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creando rúbrica: {str(e)}")
            raise
    
    @staticmethod
    def get_rubrics(teacher_id: str, include_public: bool = True) -> List[Dict[str, Any]]:
        """
        Obtiene las rúbricas de un profesor
        
        Args:
            teacher_id: ID del profesor
            include_public: Si incluir rúbricas públicas de otros profesores
            
        Returns:
            Lista de rúbricas
        """
        try:
            query = db.session.query(Rubric)
            
            if include_public:
                # Incluir rúbricas del profesor y rúbricas públicas
                query = query.filter(
                    (Rubric.teacher_id == teacher_id) | (Rubric.is_public == True)
                )
            else:
                # Solo rúbricas del profesor
                query = query.filter(Rubric.teacher_id == teacher_id)
            
            rubrics = query.order_by(Rubric.created_at.desc()).all()
            
            return [
                {
                    'id': str(rubric.id),
                    'title': rubric.title,
                    'description': rubric.description,
                    'subject': rubric.subject,
                    'grade_level': rubric.grade_level,
                    'total_points': rubric.total_points,
                    'criteria': rubric.criteria,
                    'is_template': rubric.is_template,
                    'is_public': rubric.is_public,
                    'teacher_id': str(rubric.teacher_id),
                    'created_at': rubric.created_at.isoformat() if rubric.created_at else None,
                    'updated_at': rubric.updated_at.isoformat() if rubric.updated_at else None
                }
                for rubric in rubrics
            ]
            
        except Exception as e:
            logger.error(f"Error obteniendo rúbricas: {str(e)}")
            raise
    
    @staticmethod
    def get_rubric(rubric_id: str, teacher_id: str) -> Dict[str, Any]:
        """
        Obtiene una rúbrica específica
        
        Args:
            rubric_id: ID de la rúbrica
            teacher_id: ID del profesor (para verificar permisos)
            
        Returns:
            Información de la rúbrica
        """
        try:
            rubric = db.session.query(Rubric).filter(
                (Rubric.id == rubric_id) & 
                ((Rubric.teacher_id == teacher_id) | (Rubric.is_public == True))
            ).first()
            
            if not rubric:
                raise ValueError("Rúbrica no encontrada o sin permisos")
            
            return {
                'id': str(rubric.id),
                'title': rubric.title,
                'description': rubric.description,
                'subject': rubric.subject,
                'grade_level': rubric.grade_level,
                'total_points': rubric.total_points,
                'criteria': rubric.criteria,
                'is_template': rubric.is_template,
                'is_public': rubric.is_public,
                'teacher_id': str(rubric.teacher_id),
                'created_at': rubric.created_at.isoformat() if rubric.created_at else None,
                'updated_at': rubric.updated_at.isoformat() if rubric.updated_at else None
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo rúbrica: {str(e)}")
            raise
    
    @staticmethod
    def update_rubric(rubric_id: str, teacher_id: str, rubric_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza una rúbrica
        
        Args:
            rubric_id: ID de la rúbrica
            teacher_id: ID del profesor
            rubric_data: Nuevos datos de la rúbrica
            
        Returns:
            Información actualizada de la rúbrica
        """
        try:
            rubric = db.session.query(Rubric).filter(
                Rubric.id == rubric_id,
                Rubric.teacher_id == teacher_id
            ).first()
            
            if not rubric:
                raise ValueError("Rúbrica no encontrada o sin permisos")
            
            # Actualizar campos
            if 'title' in rubric_data:
                rubric.title = rubric_data['title']
            if 'description' in rubric_data:
                rubric.description = rubric_data['description']
            if 'subject' in rubric_data:
                rubric.subject = rubric_data['subject']
            if 'grade_level' in rubric_data:
                rubric.grade_level = rubric_data['grade_level']
            if 'total_points' in rubric_data:
                rubric.total_points = rubric_data['total_points']
            if 'criteria' in rubric_data:
                rubric.criteria = rubric_data['criteria']
            if 'is_template' in rubric_data:
                rubric.is_template = rubric_data['is_template']
            if 'is_public' in rubric_data:
                rubric.is_public = rubric_data['is_public']
            
            rubric.updated_at = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"Rúbrica actualizada: {rubric.title}")
            
            return {
                'id': str(rubric.id),
                'title': rubric.title,
                'description': rubric.description,
                'subject': rubric.subject,
                'grade_level': rubric.grade_level,
                'total_points': rubric.total_points,
                'criteria': rubric.criteria,
                'is_template': rubric.is_template,
                'is_public': rubric.is_public,
                'teacher_id': str(rubric.teacher_id),
                'created_at': rubric.created_at.isoformat() if rubric.created_at else None,
                'updated_at': rubric.updated_at.isoformat() if rubric.updated_at else None
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error actualizando rúbrica: {str(e)}")
            raise
    
    @staticmethod
    def delete_rubric(rubric_id: str, teacher_id: str) -> bool:
        """
        Elimina una rúbrica
        
        Args:
            rubric_id: ID de la rúbrica
            teacher_id: ID del profesor
            
        Returns:
            True si se eliminó correctamente
        """
        try:
            rubric = db.session.query(Rubric).filter(
                Rubric.id == rubric_id,
                Rubric.teacher_id == teacher_id
            ).first()
            
            if not rubric:
                raise ValueError("Rúbrica no encontrada o sin permisos")
            
            db.session.delete(rubric)
            db.session.commit()
            
            logger.info(f"Rúbrica eliminada: {rubric.title}")
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error eliminando rúbrica: {str(e)}")
            raise
