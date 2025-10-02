#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.abspath('.'))

from src.database.models import db, User
from src.config.settings import config
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    try:
        users = User.query.all()
        print(f'Usuarios en la base de datos: {len(users)}')
        for user in users:
            print(f'- {user.email} ({user.role.value})')
        print("Conexión a base de datos exitosa!")
    except Exception as e:
        print(f"Error: {e}")
