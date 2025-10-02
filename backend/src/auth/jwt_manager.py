"""
Configuración y manejo de JWT
"""
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from datetime import timedelta
import logging

# Inicializar JWT Manager
jwt = JWTManager()

def init_jwt(app):
    """
    Inicializar JWT con la aplicación Flask
    
    :param app: Instancia de la aplicación Flask
    """
    try:
        jwt.init_app(app)
        
        # Configurar callbacks
        @jwt.user_identity_loader
        def user_identity_lookup(user):
            """Callback para obtener la identidad del usuario"""
            return user.id if hasattr(user, 'id') else str(user)
        
        @jwt.user_lookup_loader
        def user_lookup_callback(_jwt_header, jwt_data):
            """Callback para buscar el usuario por identidad"""
            from src.database.models import User
            identity = jwt_data["sub"]
            return User.query.filter_by(id=identity).one_or_none()
        
        @jwt.expired_token_loader
        def expired_token_callback(jwt_header, jwt_payload):
            """Callback para tokens expirados"""
            return {"message": "Token expirado", "error": "token_expired"}, 401
        
        @jwt.invalid_token_loader
        def invalid_token_callback(error):
            """Callback para tokens inválidos"""
            return {"message": "Token inválido", "error": "invalid_token"}, 401
        
        @jwt.unauthorized_loader
        def missing_token_callback(error):
            """Callback para tokens faltantes"""
            return {"message": "Token de acceso requerido", "error": "missing_token"}, 401
        
        logging.info("JWT Manager inicializado correctamente")
        
    except Exception as e:
        logging.error(f"Error inicializando JWT Manager: {e}")
        raise

def create_tokens(user):
    """
    Crear tokens de acceso y refresh para un usuario
    
    :param user: Usuario para el cual crear los tokens
    :return: Diccionario con access_token y refresh_token
    """
    try:
        # Crear token de acceso (válido por 1 hora)
        access_token = create_access_token(
            identity=user,
            expires_delta=timedelta(hours=1),
            additional_claims={
                "role": user.role.value,
                "username": user.username
            }
        )
        
        # Crear token de refresh (válido por 30 días)
        refresh_token = create_refresh_token(
            identity=user,
            expires_delta=timedelta(days=30)
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": 3600  # 1 hora en segundos
        }
        
    except Exception as e:
        logging.error(f"Error creando tokens: {e}")
        raise

def get_current_user():
    """
    Obtener el usuario actual desde el token JWT
    
    :return: Usuario actual o None
    """
    try:
        return get_jwt_identity()
    except Exception as e:
        logging.error(f"Error obteniendo usuario actual: {e}")
        return None

def get_user_role():
    """
    Obtener el rol del usuario actual desde el token JWT
    
    :return: Rol del usuario o None
    """
    try:
        claims = get_jwt()
        return claims.get("role")
    except Exception as e:
        logging.error(f"Error obteniendo rol del usuario: {e}")
        return None
