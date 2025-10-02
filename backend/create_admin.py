import os
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash

# Add the project root to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.database.database import db
from src.database.models import User, UserRole
from src.config.settings import config

def create_admin_user():
    # Create Flask app context
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    
    with app.app_context():
        db.init_app(app)
        
        # Check if admin user already exists
        admin_user = db.session.query(User).filter_by(email='admin@autograder.com').first()
        if admin_user:
            print("El usuario admin ya existe.")
            return

        # Create admin user
        password_hash = generate_password_hash('Admin123!')
        admin_user = User(
            email='admin@autograder.com',
            username='admin',
            password_hash=password_hash,
            first_name='Administrador',
            last_name='Sistema',
            role=UserRole.ADMIN,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Usuario admin creado exitosamente:")
        print(f"Email: {admin_user.email}")
        print(f"Password: Admin123!")

if __name__ == '__main__':
    create_admin_user()
