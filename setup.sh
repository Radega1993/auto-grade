#!/bin/bash

# Script de configuración para desarrollo de AutoGrader
# Este script configura el entorno de desarrollo completo

set -e  # Salir si hay algún error

echo "🚀 Configurando AutoGrader para desarrollo..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar prerrequisitos
check_prerequisites() {
    print_status "Verificando prerrequisitos..."
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 no está instalado"
        exit 1
    fi
    
    # Verificar Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js no está instalado"
        exit 1
    fi
    
    # Verificar Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado"
        exit 1
    fi
    
    # Verificar Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose no está instalado"
        exit 1
    fi
    
    print_status "Todos los prerrequisitos están instalados ✓"
}

# Configurar variables de entorno
setup_environment() {
    print_status "Configurando variables de entorno..."
    
    if [ ! -f .env ]; then
        cp .env.example .env
        print_status "Archivo .env creado desde .env.example"
        print_warning "Por favor, edita .env con tus configuraciones"
    else
        print_status "Archivo .env ya existe"
    fi
}

# Configurar backend
setup_backend() {
    print_status "Configurando backend..."
    
    cd backend
    
    # Crear entorno virtual si no existe
    if [ ! -d "venv" ]; then
        print_status "Creando entorno virtual..."
        python3 -m venv venv
    fi
    
    # Activar entorno virtual
    source venv/bin/activate
    
    # Instalar dependencias
    print_status "Instalando dependencias de Python..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    cd ..
    print_status "Backend configurado ✓"
}

# Configurar frontend
setup_frontend() {
    print_status "Configurando frontend..."
    
    cd frontend
    
    # Instalar dependencias
    print_status "Instalando dependencias de Node.js..."
    npm install
    
    cd ..
    print_status "Frontend configurado ✓"
}

# Levantar servicios de infraestructura
start_infrastructure() {
    print_status "Levantando servicios de infraestructura..."
    
    # Levantar solo PostgreSQL y Redis
    docker-compose -f infrastructure/docker-compose.yml up -d postgres redis
    
    # Esperar a que los servicios estén listos
    print_status "Esperando a que los servicios estén listos..."
    sleep 10
    
    print_status "Servicios de infraestructura levantados ✓"
}

# Configurar base de datos
setup_database() {
    print_status "Configurando base de datos..."
    
    cd backend
    source venv/bin/activate
    
    # Crear migración inicial
    print_status "Creando migración inicial..."
    alembic revision --autogenerate -m "Initial migration"
    
    # Aplicar migraciones
    print_status "Aplicando migraciones..."
    alembic upgrade head
    
    cd ..
    print_status "Base de datos configurada ✓"
}

# Crear directorios necesarios
create_directories() {
    print_status "Creando directorios necesarios..."
    
    mkdir -p backend/uploads
    mkdir -p backend/temp
    mkdir -p backend/logs
    
    print_status "Directorios creados ✓"
}

# Mostrar información de uso
show_usage() {
    echo ""
    echo "🎉 ¡Configuración completada!"
    echo ""
    echo "Para iniciar el desarrollo:"
    echo ""
    echo "1. Levantar servicios de infraestructura:"
    echo "   docker-compose -f infrastructure/docker-compose.yml up -d"
    echo ""
    echo "2. Iniciar backend:"
    echo "   cd backend && source venv/bin/activate && python -m src.main"
    echo ""
    echo "3. Iniciar frontend:"
    echo "   cd frontend && npm run dev"
    echo ""
    echo "4. Acceder a la aplicación:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend:  http://localhost:5000"
    echo "   API:      http://localhost:5000/api"
    echo ""
    echo "5. Usuario admin por defecto:"
    echo "   Email:    admin@autograder.com"
    echo "   Password: Admin123!"
    echo ""
    echo "Para más información, consulta docs/DEVELOPMENT.md"
}

# Función principal
main() {
    echo "🏗️  AutoGrader - Configuración de Desarrollo"
    echo "=============================================="
    echo ""
    
    check_prerequisites
    setup_environment
    create_directories
    setup_backend
    setup_frontend
    start_infrastructure
    setup_database
    show_usage
}

# Ejecutar función principal
main "$@"
