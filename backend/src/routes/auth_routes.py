from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import logging

from src.auth.decorators import jwt_required, validate_json_request
from src.auth.services import AuthService

logger = logging.getLogger(__name__)

# Crear blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
@cross_origin()
@validate_json_request(['email', 'username', 'password', 'first_name', 'last_name'])
def register(data):
    """Registra un nuevo usuario"""
    try:
        result = AuthService.register_user(data)
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'user': result
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error registrando usuario: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/login', methods=['POST'])
@cross_origin()
@validate_json_request(['email_or_username', 'password'])
def login(data):
    """Autentica un usuario"""
    try:
        result = AuthService.authenticate_user(
            data['email_or_username'],
            data['password']
        )
        
        return jsonify({
            'message': 'Login exitoso',
            'user': result['user'],
            'tokens': result['tokens']
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/profile', methods=['GET'])
@cross_origin()
@jwt_required
def get_profile():
    """Obtiene el perfil del usuario actual"""
    try:
        current_user = request.current_user
        return jsonify({
            'message': 'Perfil obtenido exitosamente',
            'user': current_user
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo perfil: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/refresh', methods=['POST'])
@cross_origin()
@validate_json_request(['refresh_token'])
def refresh_token(data):
    """Renueva el token de acceso"""
    try:
        # TODO: Implementar lógica de refresh token
        return jsonify({'error': 'Funcionalidad en desarrollo'}), 501
        
    except Exception as e:
        logger.error(f"Error renovando token: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/logout', methods=['POST'])
@cross_origin()
@jwt_required
def logout():
    """Cierra la sesión del usuario"""
    try:
        # TODO: Implementar blacklist de tokens
        return jsonify({'message': 'Logout exitoso'}), 200
        
    except Exception as e:
        logger.error(f"Error en logout: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500
