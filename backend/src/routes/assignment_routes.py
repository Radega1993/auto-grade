from flask import Blueprint, request, jsonify, current_app, Response
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import os
import logging

from ..auth.decorators import jwt_required, require_roles
from ..database.models import UserRole
from ..services.assignment_service import AssignmentService

logger = logging.getLogger(__name__)

# Crear blueprint
assignment_bp = Blueprint('assignments', __name__, url_prefix='/api/assignments')

# Inicializar servicio (se configurará en main.py)
assignment_service = None

def init_assignment_service(upload_folder: str, openai_api_key: str):
    """Inicializa el servicio de asignaciones"""
    global assignment_service
    assignment_service = AssignmentService()
    logger.info("Servicio de asignaciones inicializado")

def _check_service():
    """Verifica que el servicio esté inicializado"""
    if assignment_service is None:
        raise RuntimeError("Servicio de asignaciones no inicializado")

@assignment_bp.route('/upload', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_required
@require_roles([UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN])
def upload_assignment():
    """Sube una nueva asignación"""
    try:
        _check_service()
        
        # Verificar que se haya subido un archivo
        if 'file' not in request.files:
            return jsonify({'error': 'No se ha proporcionado archivo'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No se ha seleccionado archivo'}), 400
        
        # Obtener datos del formulario
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        
        if not title:
            return jsonify({'error': 'El título es requerido'}), 400
        
        # Obtener ID del usuario actual
        current_user = request.current_user
        teacher_id = str(current_user['id'])
        
        logger.info(f"Subiendo asignación: {title} para usuario {teacher_id}")
        
        # Crear asignación
        result = assignment_service.create_assignment_from_file(
            file=file,
            title=title,
            description=description,
            teacher_id=teacher_id
        )
        
        return jsonify({
            'message': 'Asignación creada exitosamente',
            'data': result
        }), 201
        
    except Exception as e:
        logger.error(f"Error subiendo asignación: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@assignment_bp.route('', methods=['GET'])
@assignment_bp.route('/', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required
@require_roles([UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN])
def get_assignments():
    """Obtiene todas las asignaciones del profesor"""
    try:
        _check_service()
        
        current_user = request.current_user
        teacher_id = str(current_user['id'])
        
        assignments = assignment_service.get_teacher_assignments(teacher_id)
        
        return jsonify({
            'message': 'Asignaciones obtenidas exitosamente',
            'data': assignments
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo asignaciones: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@assignment_bp.route('/<assignment_id>', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required
@require_roles([UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN])
def get_assignment(assignment_id):
    """Obtiene una asignación específica"""
    try:
        _check_service()
        
        current_user = request.current_user
        teacher_id = str(current_user['id'])
        
        assignment = assignment_service.get_assignment(assignment_id, teacher_id)
        
        if not assignment:
            return jsonify({'error': 'Asignación no encontrada'}), 404
        
        return jsonify({
            'message': 'Asignación obtenida exitosamente',
            'data': assignment
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo asignación: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@assignment_bp.route('/<assignment_id>/solutions', methods=['PUT'])
@cross_origin(supports_credentials=True)
@jwt_required
@require_roles([UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN])
def update_solutions(assignment_id):
    """Actualiza las soluciones de una asignación"""
    try:
        _check_service()
        
        data = request.get_json()
        
        if not data or 'solutions' not in data:
            return jsonify({'error': 'Se requieren las soluciones'}), 400
        
        current_user = request.current_user
        teacher_id = str(current_user['id'])
        
        result = assignment_service.update_solutions(assignment_id, data['solutions'], teacher_id)
        
        return jsonify({
            'message': 'Soluciones actualizadas exitosamente',
            'data': result
        }), 200
        
    except Exception as e:
        logger.error(f"Error actualizando soluciones: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@assignment_bp.route('/<assignment_id>/rubric', methods=['PUT'])
@cross_origin(supports_credentials=True)
@jwt_required
@require_roles([UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN])
def update_rubric(assignment_id):
    """Actualiza la rúbrica de una asignación"""
    try:
        _check_service()
        
        data = request.get_json()
        
        if not data or 'rubric' not in data:
            return jsonify({'error': 'Se requiere la rúbrica'}), 400
        
        current_user = request.current_user
        teacher_id = str(current_user['id'])
        
        result = assignment_service.update_rubric(assignment_id, data['rubric'], teacher_id)
        
        return jsonify({
            'message': 'Rúbrica actualizada exitosamente',
            'data': result
        }), 200
        
    except Exception as e:
        logger.error(f"Error actualizando rúbrica: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@assignment_bp.route('/<assignment_id>/finalize', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_required
@require_roles([UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN])
def finalize_assignment(assignment_id):
    """Finaliza una asignación (marca como lista para usar)"""
    try:
        _check_service()
        
        current_user = request.current_user
        teacher_id = str(current_user['id'])
        
        result = assignment_service.finalize_assignment(assignment_id, teacher_id)
        
        return jsonify({
            'message': 'Asignación finalizada exitosamente',
            'data': result
        }), 200
        
    except Exception as e:
        logger.error(f"Error finalizando asignación: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@assignment_bp.route('/check-stuck', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_required
@require_roles([UserRole.ADMIN])
def check_stuck_assignments():
    """Verifica y marca como error las asignaciones bloqueadas"""
    try:
        count = assignment_service.check_stuck_assignments()
        return jsonify({
            'message': f'Verificación completada',
            'stuck_assignments_fixed': count
        }), 200
        
    except Exception as e:
        logger.error(f"Error verificando asignaciones bloqueadas: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@assignment_bp.route('/<assignment_id>/delete', methods=['DELETE'])
@cross_origin(supports_credentials=True)
@jwt_required
@require_roles([UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN])
def delete_assignment(assignment_id: str):
    """Elimina una asignación"""
    try:
        current_user = request.current_user
        teacher_id = str(current_user['id'])
        
        result = assignment_service.delete_assignment(assignment_id, teacher_id)
        
        if 'error' in result:
            return jsonify(result), 404
            
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error eliminando asignación {assignment_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@assignment_bp.route('/<assignment_id>/download-rubric', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required
@require_roles([UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN])
def download_rubric(assignment_id: str):
    """Descarga la rúbrica en formato PDF"""
    try:
        current_user = request.current_user
        teacher_id = str(current_user['id'])
        
        pdf_data = assignment_service.generate_rubric_pdf(assignment_id, teacher_id)
        
        if 'error' in pdf_data:
            return jsonify(pdf_data), 404
            
        return Response(
            pdf_data['pdf_content'],
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename="{pdf_data["filename"]}"'
            }
        )
        
    except Exception as e:
        logger.error(f"Error generando PDF de rúbrica {assignment_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@assignment_bp.route('/<assignment_id>/download-solutions', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required
@require_roles([UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN])
def download_solutions(assignment_id: str):
    """Descarga las soluciones en formato PDF"""
    try:
        current_user = request.current_user
        teacher_id = str(current_user['id'])
        
        pdf_data = assignment_service.generate_solutions_pdf(assignment_id, teacher_id)
        
        if 'error' in pdf_data:
            return jsonify(pdf_data), 404
            
        return Response(
            pdf_data['pdf_content'],
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename="{pdf_data["filename"]}"'
            }
        )
        
    except Exception as e:
        logger.error(f"Error generando PDF de soluciones {assignment_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500
