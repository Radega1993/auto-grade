# 🎓 AutoGrader - Corrección Automática de Tareas con IA

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18.3.1-blue.svg)](https://reactjs.org)
[![Flask](https://img.shields.io/badge/Flask-2.1.0-green.svg)](https://flask.palletsprojects.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

## 🚀 Visión del Producto

AutoGrader es una plataforma SaaS innovadora que utiliza inteligencia artificial para automatizar la corrección de tareas educativas, ahorrando tiempo a profesores y proporcionando retroalimentación instantánea y detallada a estudiantes.

## ✨ Características Principales

- 🤖 **Corrección Automática con IA**: Utiliza Ollama (Llama3.2) y OpenAI (GPT-4)
- 📄 **Soporte Multi-formato**: PDF, DOCX, TXT, Markdown
- 🔍 **Detección de IA**: Identifica contenido generado por inteligencia artificial
- 📊 **Análisis de Similitud**: Detecta plagio entre tareas
- 🎯 **Rúbricas Personalizables**: Criterios de evaluación configurables
- 👥 **Sistema de Roles**: Profesores, Coordinadores y Administradores
- 🔐 **Autenticación JWT**: Sistema seguro de autenticación
- 📈 **Dashboard y Estadísticas**: Panel de control completo
- 🌐 **API REST**: Endpoints documentados para integraciones

## 🛠️ Stack Tecnológico

### Backend
- **Framework**: Flask 2.1.0
- **Lenguaje**: Python 3.10+
- **Base de Datos**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0.36
- **Autenticación**: JWT con Flask-JWT-Extended
- **IA**: Ollama + Llama3.2, OpenAI GPT-4
- **Cache**: Redis 7
- **Migraciones**: Alembic

### Frontend
- **Framework**: React 18.3.1
- **Lenguaje**: TypeScript 5.6.2
- **Estilos**: TailwindCSS 3.4.16
- **HTTP Client**: Axios 1.7.9
- **Bundler**: Vite 6.0.1

### Infraestructura
- **Contenedores**: Docker + Docker Compose
- **Proxy**: Nginx
- **Monitoreo**: Logging estructurado
- **CI/CD**: GitHub Actions (próximamente)

## 🚀 Instalación Rápida

### Prerrequisitos
- Docker y Docker Compose
- Python 3.10+
- Node.js 16+
- Git

### Configuración Automática

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/auto-grader.git
cd auto-grader

# Ejecutar script de configuración
./setup.sh
```

### Configuración Manual

#### 1. Configurar Variables de Entorno
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

#### 2. Levantar Servicios
```bash
# Levantar infraestructura
docker-compose -f infrastructure/docker-compose.yml up -d

# Configurar backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python -m src.main

# Configurar frontend
cd frontend
npm install
npm run dev
```

## 📖 Documentación

- [📋 Análisis del Proyecto](docs/PROJECT_ANALYSIS.md)
- [🏗️ Arquitectura](docs/ARCHITECTURE.md)
- [🚀 Guía de Desarrollo](docs/DEVELOPMENT.md)
- [🗺️ Roadmap](docs/ROADMAP.md)

## 🔧 Desarrollo

### Comandos Útiles

```bash
# Backend
cd backend
source venv/bin/activate
python -m src.main              # Ejecutar servidor
pytest                          # Ejecutar tests
alembic upgrade head           # Aplicar migraciones

# Frontend
cd frontend
npm run dev                    # Servidor de desarrollo
npm run build                  # Build para producción
npm test                       # Ejecutar tests

# Docker
docker-compose -f infrastructure/docker-compose.yml up    # Levantar servicios
docker-compose -f infrastructure/docker-compose.yml down  # Parar servicios
```

### Estructura del Proyecto

```
auto-grader/
├── backend/                   # API Flask
│   ├── src/
│   │   ├── auth/             # Autenticación JWT
│   │   ├── database/         # Modelos y BD
│   │   ├── routes/           # Endpoints API
│   │   ├── services/         # Lógica de negocio
│   │   └── utils/            # Utilidades
│   └── migrations/           # Migraciones de BD
├── frontend/                 # Aplicación React
│   ├── src/
│   │   ├── components/       # Componentes React
│   │   ├── pages/           # Páginas
│   │   └── services/        # Servicios API
├── infrastructure/           # Docker y configuración
└── docs/                    # Documentación
```

## 🔐 Autenticación

### Usuario Admin por Defecto
- **Email**: admin@autograder.com
- **Password**: Admin123!

### Roles de Usuario
- **Teacher**: Puede crear tareas y obtener correcciones
- **Coordinator**: Gestiona profesores dentro de una institución
- **Admin**: Gestión completa del sistema

## 📊 API Endpoints

### Autenticación
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/profile` - Obtener perfil
- `POST /api/auth/refresh` - Renovar token

### Tareas
- `POST /api/assignments/correct` - Corregir tareas
- `GET /api/assignments` - Listar tareas
- `GET /api/assignments/{id}` - Obtener tarea específica

## 🧪 Testing

```bash
# Tests unitarios
pytest

# Tests con cobertura
pytest --cov=src

# Tests de integración
pytest tests/integration/

# Tests E2E (próximamente)
npm run test:e2e
```

## 🚀 Despliegue

### Desarrollo
```bash
docker-compose -f infrastructure/docker-compose.yml up --build
```

### Producción
```bash
# Configurar variables de entorno de producción
export FLASK_ENV=production
export SECRET_KEY=tu-clave-secreta-segura
export JWT_SECRET_KEY=tu-jwt-secreto-seguro

# Levantar con perfil de producción
docker-compose -f infrastructure/docker-compose.yml --profile production up -d
```

## 📈 Roadmap

### ✅ Completado (Sprint 1)
- [x] Infraestructura base con Docker
- [x] Base de datos PostgreSQL con SQLAlchemy
- [x] Sistema de autenticación JWT
- [x] Documentación técnica básica
- [x] Variables de entorno configuradas

### 🚧 En Progreso (Sprint 2)
- [ ] Dashboard básico con estadísticas
- [ ] Historial de correcciones
- [ ] Gestión de usuarios y roles
- [ ] Tests unitarios completos
- [ ] CI/CD básico

### 📋 Próximos Sprints
- [ ] Optimización de rendimiento
- [ ] Sistema de colas con Redis
- [ ] UI/UX mejorado
- [ ] Tests E2E
- [ ] Funcionalidades avanzadas

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Equipo

- **Desarrollador Principal**: [Tu Nombre]
- **Project Manager**: [Nombre del PM]
- **Experto en IA**: [Nombre del Experto]

## 📞 Soporte

- **Email**: soporte@autograder.com
- **Documentación**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/tu-usuario/auto-grader/issues)

---

**Desarrollado con ❤️ para la educación**
