# 🏗️ Arquitectura del Sistema AutoGrader

## Visión General

AutoGrader es una plataforma SaaS que utiliza inteligencia artificial para automatizar la corrección de tareas educativas. La arquitectura está diseñada para ser escalable, mantenible y segura.

## Arquitectura de Alto Nivel

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Base de       │
│   (React)       │◄──►│   (Flask)       │◄──►│   Datos         │
│                 │    │                 │    │   (PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx         │    │   Redis         │    │   Ollama        │
│   (Reverse      │    │   (Cache)       │    │   (IA Local)    │
│   Proxy)        │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Componentes del Sistema

### 1. Frontend (React + TypeScript)
- **Tecnología**: React 18, TypeScript, TailwindCSS
- **Responsabilidades**:
  - Interfaz de usuario para subir tareas
  - Visualización de resultados de corrección
  - Gestión de usuarios y autenticación
  - Dashboard con estadísticas

### 2. Backend (Flask + Python)
- **Tecnología**: Flask, SQLAlchemy, JWT
- **Responsabilidades**:
  - API REST para comunicación con frontend
  - Procesamiento de archivos (PDF, DOCX, TXT)
  - Integración con modelos de IA
  - Autenticación y autorización
  - Gestión de base de datos

### 3. Base de Datos (PostgreSQL)
- **Tecnología**: PostgreSQL 15
- **Responsabilidades**:
  - Almacenamiento de usuarios y perfiles
  - Gestión de tareas y correcciones
  - Rúbricas de evaluación
  - Historial de actividades

### 4. Cache (Redis)
- **Tecnología**: Redis 7
- **Responsabilidades**:
  - Cache de respuestas de IA
  - Sesiones de usuario
  - Datos temporales

### 5. IA Local (Ollama)
- **Tecnología**: Ollama + Llama3.2
- **Responsabilidades**:
  - Corrección automática de tareas
  - Detección de contenido generado por IA
  - Análisis de similitud entre tareas

## Patrones de Diseño Implementados

### 1. Strategy Pattern
- **Ubicación**: `src/models/model_strategy.py`
- **Propósito**: Intercambiar entre diferentes modelos de IA (Ollama, OpenAI)
- **Beneficios**: Flexibilidad para usar diferentes proveedores de IA

### 2. Repository Pattern
- **Ubicación**: `src/database/models.py`
- **Propósito**: Abstracción de acceso a datos
- **Beneficios**: Separación de lógica de negocio y acceso a datos

### 3. Service Layer Pattern
- **Ubicación**: `src/services/`
- **Propósito**: Lógica de negocio centralizada
- **Beneficios**: Reutilización de código y mantenibilidad

## Flujo de Datos

### 1. Proceso de Corrección de Tareas

```
Usuario sube archivo → Validación → Extracción de texto → 
Análisis con IA → Generación de comentarios → Almacenamiento → 
Respuesta al usuario
```

### 2. Autenticación

```
Login → Validación de credenciales → Generación de JWT → 
Almacenamiento en Redis → Respuesta con tokens
```

## Seguridad

### 1. Autenticación
- JWT tokens para autenticación stateless
- Refresh tokens para renovación automática
- Validación de contraseñas con criterios de seguridad

### 2. Autorización
- Sistema de roles (Teacher, Coordinator, Admin)
- Decoradores para protección de endpoints
- Validación de permisos por recurso

### 3. Validación de Datos
- Validación de entrada en todos los endpoints
- Sanitización de archivos subidos
- Límites de tamaño de archivo

## Escalabilidad

### 1. Horizontal
- Microservicios preparados para contenedores
- Load balancing con Nginx
- Base de datos con réplicas de lectura

### 2. Vertical
- Cache Redis para optimización
- Procesamiento asíncrono de tareas largas
- Compresión de archivos

## Monitoreo y Observabilidad

### 1. Logging
- Logs estructurados con niveles configurables
- Rotación automática de archivos de log
- Integración con sistemas de monitoreo

### 2. Métricas
- Tiempo de respuesta de API
- Uso de recursos del sistema
- Métricas de IA (precisión, tiempo de procesamiento)

## Despliegue

### 1. Desarrollo
- Docker Compose para entorno local
- Hot reload para desarrollo
- Base de datos en contenedor

### 2. Producción
- Docker containers orquestados
- Nginx como reverse proxy
- SSL/TLS para comunicación segura
- Backup automático de base de datos

## Consideraciones de Rendimiento

### 1. Optimizaciones de Base de Datos
- Índices en campos de búsqueda frecuente
- Consultas optimizadas con SQLAlchemy
- Connection pooling

### 2. Cache
- Cache de respuestas de IA similares
- Cache de sesiones de usuario
- Cache de datos de configuración

### 3. Procesamiento Asíncrono
- Colas para tareas de corrección largas
- Procesamiento en paralelo de múltiples tareas
- Timeout y retry logic

## Tecnologías Utilizadas

### Backend
- **Framework**: Flask 2.1.0
- **ORM**: SQLAlchemy 2.0.36
- **Autenticación**: Flask-JWT-Extended 4.6.0
- **Migraciones**: Alembic 1.13.1
- **Cache**: Redis 5.0.1

### Frontend
- **Framework**: React 18.3.1
- **Lenguaje**: TypeScript 5.6.2
- **Estilos**: TailwindCSS 3.4.16
- **HTTP Client**: Axios 1.7.9

### Infraestructura
- **Contenedores**: Docker
- **Orquestación**: Docker Compose
- **Base de Datos**: PostgreSQL 15
- **Cache**: Redis 7
- **IA**: Ollama + Llama3.2

## Próximos Pasos

1. **Microservicios**: Separar servicios en contenedores independientes
2. **API Gateway**: Implementar gateway para gestión centralizada
3. **Message Queue**: Añadir RabbitMQ o Apache Kafka
4. **Monitoring**: Integrar Prometheus y Grafana
5. **CI/CD**: Pipeline automatizado con GitHub Actions
