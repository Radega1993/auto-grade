from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
import logging

from src.config.settings import config
from src.database.database import db
from src.auth.jwt_manager import jwt, init_jwt
from src.routes.auth_routes import auth_bp
from src.routes.assignment_routes import assignment_bp, init_assignment_service

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': config.SQLALCHEMY_DATABASE_URI,
        'SQLALCHEMY_TRACK_MODIFICATIONS': config.SQLALCHEMY_TRACK_MODIFICATIONS,
        'JWT_SECRET_KEY': config.JWT_SECRET_KEY,
        'SECRET_KEY': config.SECRET_KEY
    })
    
    # CORS - Configuración más permisiva para desarrollo
    CORS(app, 
         origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:3000", "http://127.0.0.1:3001", "http://127.0.0.1:5173", "http://127.0.0.1:5174"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept", "Origin"],
         supports_credentials=True,
         expose_headers=["Content-Type", "Authorization"])
    
    # Inicializar extensiones
    db.init_app(app)
    init_jwt(app)  # Inicializar JWT correctamente
    
    # Crear tablas
    with app.app_context():
        db.create_all()
        logger.info("Base de datos inicializada")
    
    # Inicializar servicios
    upload_folder = config.UPLOAD_FOLDER
    openai_api_key = config.OPENAI_API_KEY
    
    if not openai_api_key:
        logger.warning("OPENAI_API_KEY no configurada. Funcionalidad de IA limitada.")
    
    init_assignment_service(upload_folder, openai_api_key)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(assignment_bp)
    
    # Ruta de salud
    @app.route('/health')
    @cross_origin()
    def health():
        return jsonify({'status': 'healthy', 'message': 'AutoGrader API funcionando'})
    
    # Manejo de errores
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint no encontrado'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
