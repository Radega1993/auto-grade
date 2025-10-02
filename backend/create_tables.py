import os
import sys
sys.path.append('.')

from flask import Flask
from src.database.database import db
from src.database.models import Base
from src.config.settings import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    try:
        db.create_all()
        print('✅ Tablas creadas exitosamente')
    except Exception as e:
        print(f'❌ Error creando tablas: {e}')
