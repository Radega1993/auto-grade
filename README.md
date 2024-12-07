# AutoGrader - Corrección Automática de Tareas con IA

## 🚀 Visión del Producto

AutoGrader es una plataforma innovadora que utiliza inteligencia artificial para automatizar la corrección de tareas educativas, ahorrando tiempo a profesores y proporcionando retroalimentación instantánea a estudiantes.

## 🌟 Características Principales

- Carga de archivos de criterios de evaluación
- Corrección automática de tareas con IA
- Generación de comentarios y calificaciones
- Interfaz de usuario intuitiva

## 🛠 Tecnologías

- **Frontend**: React + TypeScript
- **Backend**: Python (Flask)
- **IA**: Ollama (Llama2)
- **Infraestructura**: Docker, Terraform
- **CI/CD**: GitHub Actions

## 📦 Instalación Rápida

### Requisitos Previos
- Docker
- Docker Compose
- Python 3.10+
- Node.js 16+

### Pasos de Instalación

1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/auto-grader.git
cd auto-grader
```

2. Levantar servicios con Docker
```bash
docker-compose up --build
```

## 🧪 Desarrollo

### Configuración de Desarrollo Local

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## 🚀 Despliegue

Ver `docs/DEPLOYMENT.md` para detalles de despliegue en diferentes entornos.

## 📈 Roadmap

- [x] MVP Básico
- [ ] Autenticación de Usuarios
- [ ] Soporte Multi-Idioma
- [ ] Integración con Plataformas Educativas

## 👥 Contribución

Por favor lee `CONTRIBUTING.md` para detalles sobre nuestro código de conducta.

## 📄 Licencia

Este proyecto está bajo licencia MIT.
```
