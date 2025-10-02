import logging
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

from ..database.database import db
from ..database.models import User, UserRole

logger = logging.getLogger(__name__)

class AuthService:
    """Servicio para manejar autenticación de usuarios"""
    
    @staticmethod
    def register_user(user_data: dict) -> dict:
        """
        Registra un nuevo usuario
        
        Args:
            user_data: Datos del usuario (email, username, password, etc.)
            
        Returns:
            Dict con información del usuario creado
        """
        try:
            # Verificar si el usuario ya existe
            existing_user = db.session.query(User).filter(
                (User.email == user_data['email']) | 
                (User.username == user_data['username'])
            ).first()
            
            if existing_user:
                if existing_user.email == user_data['email']:
                    raise ValueError("El email ya está registrado")
                else:
                    raise ValueError("El nombre de usuario ya está en uso")
            
            # Crear nuevo usuario
            password_hash = generate_password_hash(user_data['password'])
            
            new_user = User(
                email=user_data['email'],
                username=user_data['username'],
                password_hash=password_hash,
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data.get('role', UserRole.TEACHER),
                is_active=True
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            logger.info(f"Usuario registrado: {new_user.email}")
            
            return {
                'id': str(new_user.id),
                'email': new_user.email,
                'username': new_user.username,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'role': new_user.role.value,  # Convertir enum a string
                'is_active': new_user.is_active,
                'created_at': new_user.created_at.isoformat() if new_user.created_at else None
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error registrando usuario: {str(e)}")
            raise
    
    @staticmethod
    def authenticate_user(email_or_username: str, password: str) -> dict:
        """
        Autentica un usuario
        
        Args:
            email_or_username: Email o nombre de usuario
            password: Contraseña
            
        Returns:
            Dict con información del usuario y tokens
        """
        try:
            # Buscar usuario por email o username
            user = db.session.query(User).filter(
                (User.email == email_or_username) | 
                (User.username == email_or_username)
            ).first()
            
            if not user:
                raise ValueError("Credenciales inválidas")
            
            if not user.is_active:
                raise ValueError("Usuario inactivo")
            
            if not check_password_hash(user.password_hash, password):
                raise ValueError("Credenciales inválidas")
            
            # Crear tokens
            access_token = create_access_token(
                identity=str(user.id),
                expires_delta=timedelta(hours=1)
            )
            
            refresh_token = create_refresh_token(
                identity=str(user.id),
                expires_delta=timedelta(days=30)
            )
            
            logger.info(f"Usuario autenticado: {user.email}")
            
            return {
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role.value,  # Convertir enum a string
                    'is_active': user.is_active,
                    'created_at': user.created_at.isoformat() if user.created_at else None
                },
                'tokens': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'token_type': 'Bearer',
                    'expires_in': 3600
                }
            }
            
        except Exception as e:
            logger.error(f"Error autenticando usuario: {str(e)}")
            raise
    
    @staticmethod
    def get_user_by_id(user_id: str) -> dict:
        """
        Obtiene un usuario por ID
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Dict con información del usuario
        """
        try:
            user = db.session.query(User).filter(User.id == user_id).first()
            
            if not user:
                raise ValueError("Usuario no encontrado")
            
            return {
                'id': str(user.id),
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role.value,  # Convertir enum a string
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo usuario: {str(e)}")
            raise
