import logging
from flask import Flask
from flask_cors import CORS
from src.config.settings import config
from src.routes.assignment_routes import assignment_bp
import os
import sys
from concurrent.futures import ProcessPoolExecutor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
executor = ProcessPoolExecutor(max_workers=os.cpu_count())

def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
    app.config['SECRET_KEY'] = config.SECRET_KEY
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s'
    )

    app.register_blueprint(assignment_bp, url_prefix='/api/assignments')
    return app

def main():
    app = create_app()
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )

if __name__ == '__main__':
    main()