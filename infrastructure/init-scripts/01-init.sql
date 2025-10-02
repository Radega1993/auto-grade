-- Script de inicialización de base de datos
-- Este script se ejecuta automáticamente al crear el contenedor de PostgreSQL

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Comentarios en tablas (se ejecutarán después de crear las tablas)
-- COMMENT ON TABLE users IS 'Usuarios del sistema (profesores, coordinadores, administradores)';
-- COMMENT ON TABLE assignments IS 'Tareas subidas por los usuarios';
-- COMMENT ON TABLE corrections IS 'Correcciones generadas por IA';
-- COMMENT ON TABLE rubrics IS 'Rúbricas de evaluación';

-- Comentarios en columnas importantes (se ejecutarán después de crear las tablas)
-- COMMENT ON COLUMN users.role IS 'Rol del usuario: teacher, coordinator, admin';
-- COMMENT ON COLUMN assignments.status IS 'Estado de la tarea: pending, processing, completed, error';
-- COMMENT ON COLUMN corrections.grade IS 'Calificación de 0 a 10';
-- COMMENT ON COLUMN corrections.ai_generated_percentage IS 'Porcentaje estimado de contenido generado por IA';
