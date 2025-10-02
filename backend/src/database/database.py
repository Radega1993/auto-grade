from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from contextlib import contextmanager

# Inicializar SQLAlchemy
db = SQLAlchemy()

# Inicializar Migrate
migrate = Migrate()

def init_db(app):
    """Inicializa la base de datos"""
    db.init_app(app)
    migrate.init_app(app, db)
    return db

@contextmanager
def session_scope():
    """Context manager para manejar sesiones de base de datos"""
    try:
        yield db.session
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()

def create_all():
    """Crear todas las tablas"""
    db.create_all()

def drop_all():
    """Eliminar todas las tablas"""
    db.drop_all()
