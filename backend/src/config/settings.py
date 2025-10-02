import os
from dataclasses import dataclass, field
from typing import List, Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

@dataclass
class Config:
    """Configuraciones centralizadas de la aplicación"""
    
    # Configuraciones del servidor
    HOST: str = field(default_factory=lambda: os.getenv('HOST', '0.0.0.0'))
    PORT: int = field(default_factory=lambda: int(os.getenv('PORT', '5000')))
    DEBUG: bool = field(default_factory=lambda: os.getenv('FLASK_ENV', 'development') == 'development')
    
    # Base de datos
    DATABASE_URL: str = field(default_factory=lambda: os.getenv('DATABASE_URL', 'postgresql://autograder_user:autograder_password@localhost:5432/autograder'))
    SQLALCHEMY_DATABASE_URI: str = field(default_factory=lambda: os.getenv('DATABASE_URL', 'postgresql://autograder_user:autograder_password@localhost:5432/autograder'))
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    
    # Redis
    REDIS_URL: str = field(default_factory=lambda: os.getenv('REDIS_URL', 'redis://localhost:6379/0'))
    
    # Configuraciones de Ollama
    OLLAMA_MODEL: str = field(default_factory=lambda: os.getenv('OLLAMA_MODEL', 'llama3.2'))
    OLLAMA_HOST: str = field(default_factory=lambda: os.getenv('OLLAMA_HOST', 'localhost'))
    OLLAMA_PORT: int = field(default_factory=lambda: int(os.getenv('OLLAMA_PORT', '11434')))
    
    # Configuraciones de OpenAI
    OPENAI_API_KEY: str = field(default_factory=lambda: os.getenv('OPENAI_API_KEY', ''))
    OPENAI_MODEL: str = field(default_factory=lambda: os.getenv('OPENAI_MODEL', 'gpt-4'))
    
    # JWT
    JWT_SECRET_KEY: str = field(default_factory=lambda: os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-change-in-production'))
    JWT_ACCESS_TOKEN_EXPIRES: int = field(default_factory=lambda: int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '3600')))
    JWT_REFRESH_TOKEN_EXPIRES: int = field(default_factory=lambda: int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', '2592000')))
    
    # Directorios
    UPLOAD_FOLDER: str = field(default_factory=lambda: os.getenv('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads')))
    TEMP_FOLDER: str = field(default_factory=lambda: os.getenv('TEMP_FOLDER', os.path.join(os.getcwd(), 'temp')))
    LOG_FOLDER: str = field(default_factory=lambda: os.path.join(os.getcwd(), 'logs'))
    
    # Límites de archivo
    MAX_CONTENT_LENGTH: int = field(default_factory=lambda: int(os.getenv('MAX_CONTENT_LENGTH', '16777216')))  # 16MB
    
    # Extensiones permitidas
    ALLOWED_EXTENSIONS: List[str] = field(default_factory=lambda: ['txt', 'pdf', 'docx', 'md', 'json'])
    
    # Configuraciones de seguridad
    SECRET_KEY: str = field(default_factory=lambda: os.getenv('SECRET_KEY', 'development_secret_key'))
    
    # Configuraciones de evaluación
    MAX_GRADE: float = 10.0
    MIN_GRADE: float = 0.0
    
    # Logging
    LOG_LEVEL: str = field(default_factory=lambda: os.getenv('LOG_LEVEL', 'INFO'))
    LOG_FILE: str = field(default_factory=lambda: os.getenv('LOG_FILE', 'logs/autograder.log'))
    
    def __post_init__(self):
        """
        Crear directorios necesarios y validar configuraciones
        """
        # Crear directorios
        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(self.TEMP_FOLDER, exist_ok=True)
        os.makedirs(self.LOG_FOLDER, exist_ok=True)
        
        # Validaciones
        self._validate_configuration()
    
    def _validate_configuration(self):
        """
        Validar configuraciones críticas
        """
        # Validar puerto de Ollama
        if not (0 < self.OLLAMA_PORT < 65536):
            raise ValueError(f"Puerto de Ollama inválido: {self.OLLAMA_PORT}")
        
        # Validar longitud máxima de archivo
        if self.MAX_CONTENT_LENGTH <= 0:
            raise ValueError(f"Longitud máxima de archivo inválida: {self.MAX_CONTENT_LENGTH}")
        
        # Validar extensiones
        if not self.ALLOWED_EXTENSIONS:
            raise ValueError("Debe haber al menos una extensión de archivo permitida")
        
        # Validar claves secretas en producción
        if not self.DEBUG:
            if self.SECRET_KEY == 'development_secret_key':
                raise ValueError("SECRET_KEY debe cambiarse en producción")
            if self.JWT_SECRET_KEY == 'your-jwt-secret-key-change-in-production':
                raise ValueError("JWT_SECRET_KEY debe cambiarse en producción")
    
    def validate_file_extension(self, filename: str) -> bool:
        """
        Validar extensión de archivo
        
        :param filename: Nombre del archivo
        :return: True si la extensión está permitida, False en caso contrario
        """
        return (
            '.' in filename and 
            filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
        )

# Crear instancia de configuración
config = Config()
