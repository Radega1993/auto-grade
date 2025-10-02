from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Integer, Float, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from .database import db

class UserRole(enum.Enum):
    TEACHER = "teacher"
    COORDINATOR = "coordinator"
    ADMIN = "admin"

class AssignmentStatus(enum.Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    AI_ANALYZED = "ai_analyzed"
    READY_FOR_EDITING = "ready_for_editing"
    FINALIZED = "finalized"
    ERROR = "error"

class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.TEACHER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    assignments = relationship("Assignment", back_populates="teacher")
    rubrics = relationship("Rubric", back_populates="teacher")
    corrections = relationship("Correction", back_populates="teacher")

class Assignment(db.Model):
    __tablename__ = 'assignments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    total_points = Column(Float, nullable=False, default=100.0)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    # Contenido extraído del archivo
    extracted_content = Column(JSON)
    
    # Análisis de IA
    ai_analysis = Column(JSON)
    
    # Soluciones y rúbrica finales (editables)
    final_solutions = Column(JSON)
    final_rubric = Column(JSON)
    
    # Estado del flujo
    status = Column(SQLEnum(AssignmentStatus), default=AssignmentStatus.UPLOADED, nullable=False)
    
    # Metadatos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    teacher = relationship("User", back_populates="assignments")
    corrections = relationship("Correction", back_populates="assignment")

class Rubric(db.Model):
    __tablename__ = 'rubrics'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    subject = Column(String(100))
    grade_level = Column(String(50))
    total_points = Column(Float, nullable=False, default=100.0)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    # Estructura de la rúbrica
    criteria = Column(JSON, nullable=False)  # Array de criterios con niveles de desempeño
    
    # Metadatos
    is_template = Column(Boolean, default=False, nullable=False)  # Si es una plantilla reutilizable
    is_public = Column(Boolean, default=False, nullable=False)    # Si es pública para otros profesores
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    teacher = relationship("User", back_populates="rubrics")
    corrections = relationship("Correction", back_populates="rubric")

class Correction(db.Model):
    __tablename__ = 'corrections'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assignment_id = Column(UUID(as_uuid=True), ForeignKey('assignments.id'), nullable=False)
    rubric_id = Column(UUID(as_uuid=True), ForeignKey('rubrics.id'), nullable=True)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    # Información del estudiante
    student_name = Column(String(255), nullable=False)
    student_file_path = Column(String(500))
    
    # Resultados de la corrección
    total_score = Column(Float, nullable=False, default=0.0)
    max_score = Column(Float, nullable=False, default=100.0)
    percentage = Column(Float, nullable=False, default=0.0)
    
    # Detalles de la corrección
    correction_details = Column(JSON)  # Detalles por ejercicio/criterio
    feedback = Column(Text)            # Comentarios generales
    suggestions = Column(Text)         # Sugerencias de mejora
    
    # Metadatos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    assignment = relationship("Assignment", back_populates="corrections")
    rubric = relationship("Rubric", back_populates="corrections")
    teacher = relationship("User", back_populates="corrections")

# Crear la instancia Base para Alembic
Base = db.Model
