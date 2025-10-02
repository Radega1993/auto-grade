"""
Decoradores para autenticación y autorización
"""
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import jwt_required as flask_jwt_required, get_jwt_identity, get_jwt
from src.database.models import User, UserRole
import logging

def jwt_required(f):
    """
    Decorador para requerir token JWT válido
    """
    @wraps(f)
    @flask_jwt_required()
    def decorated(*args, **kwargs):
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.filter_by(id=current_user_id).first()
            
            if not current_user or not current_user.is_active:
                return jsonify({"message": "Usuario no válido o inactivo"}), 401
            
            # Agregar usuario actual a request para acceso fácil
            request.current_user = {
                'id': str(current_user.id),
                'email': current_user.email,
                'username': current_user.username,
                'role': current_user.role,
                'first_name': current_user.first_name,
                'last_name': current_user.last_name
            }
            
            return f(*args, **kwargs)
            
        except Exception as e:
            logging.error(f"Error en jwt_required: {e}")
            return jsonify({"message": "Error de autenticación"}), 401
    
    return decorated

def require_roles(roles):
    """
    Decorador para requerir roles específicos
    
    Args:
        roles: Lista de roles permitidos
    """
    def decorator(f):
        @wraps(f)
        @jwt_required
        def decorated(*args, **kwargs):
            try:
                current_user = request.current_user
                
                if current_user['role'] not in roles:
                    return jsonify({
                        "message": "No tienes permisos para acceder a este recurso"
                    }), 403
                
                return f(*args, **kwargs)
                
            except Exception as e:
                logging.error(f"Error en require_roles: {e}")
                return jsonify({"message": "Error de autorización"}), 403
        
        return decorated
    return decorator

def admin_required(f):
    """
    Decorador para requerir rol de administrador
    """
    @wraps(f)
    @jwt_required
    def decorated(*args, **kwargs):
        try:
            current_user = request.current_user
            
            if current_user['role'] != UserRole.ADMIN:
                return jsonify({"message": "Se requiere rol de administrador"}), 403
            
            return f(*args, **kwargs)
            
        except Exception as e:
            logging.error(f"Error en admin_required: {e}")
            return jsonify({"message": "Error de autorización"}), 403
    
    return decorated

def teacher_required(f):
    """
    Decorador para requerir rol de profesor o superior
    """
    @wraps(f)
    @jwt_required
    def decorated(*args, **kwargs):
        try:
            current_user = request.current_user
            
            if current_user['role'] not in [UserRole.TEACHER, UserRole.COORDINATOR, UserRole.ADMIN]:
                return jsonify({"message": "Se requiere rol de profesor o superior"}), 403
            
            return f(*args, **kwargs)
            
        except Exception as e:
            logging.error(f"Error en teacher_required: {e}")
            return jsonify({"message": "Error de autorización"}), 403
    
    return decorated

def coordinator_required(f):
    """
    Decorador para requerir rol de coordinador o superior
    """
    @wraps(f)
    @jwt_required
    def decorated(*args, **kwargs):
        try:
            current_user = request.current_user
            
            if current_user['role'] not in [UserRole.COORDINATOR, UserRole.ADMIN]:
                return jsonify({"message": "Se requiere rol de coordinador o superior"}), 403
            
            return f(*args, **kwargs)
            
        except Exception as e:
            logging.error(f"Error en coordinator_required: {e}")
            return jsonify({"message": "Error de autorización"}), 403
    
    return decorated

def validate_json_request(required_fields=None):
    """
    Decorador para validar que la petición sea JSON y contenga campos requeridos
    
    :param required_fields: Lista de campos requeridos
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                if not request.is_json:
                    return jsonify({"message": "Se requiere contenido JSON"}), 400
                
                data = request.get_json()
                
                if required_fields:
                    missing_fields = [field for field in required_fields if field not in data]
                    if missing_fields:
                        return jsonify({
                            "message": "Campos requeridos faltantes",
                            "missing_fields": missing_fields
                        }), 400
                
                # Agregar datos JSON a los argumentos
                return f(data, *args, **kwargs)
                
            except Exception as e:
                logging.error(f"Error en validate_json_request: {e}")
                return jsonify({"message": "Error validando petición"}), 400
        
        return decorated
    return decorator
