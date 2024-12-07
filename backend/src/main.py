import logging

from flask import Flask
from flask_cors import CORS

from src.config.settings import config
from src.routes.assignment_routes import assignment_bp
from concurrent.futures import ProcessPoolExecutor
import os
import sys

# Configuración del path para que src sea reconocible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

executor = ProcessPoolExecutor(max_workers=os.cpu_count())

def create_app():
    """Factory de aplicación Flask"""
    app = Flask(__name__)
    
    # Configuraciones
    app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
    app.config['SECRET_KEY'] = config.SECRET_KEY
    
    # CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s'
    )
    
    # Registrar blueprints
    app.register_blueprint(assignment_bp, url_prefix='/api/assignments')
    
    return app

def main():
    """Iniciar servidor"""
    app = create_app()
    app.run(
        host=config.HOST, 
        port=config.PORT, 
        debug=config.DEBUG
    )

if __name__ == '__main__':
    main()