# 🚀 Guía de Desarrollo - AutoGrader

## Configuración del Entorno de Desarrollo

### Prerrequisitos

- Python 3.10+
- Node.js 16+
- Docker y Docker Compose
- Git

### Instalación Local

#### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/auto-grader.git
cd auto-grader
```

#### 2. Configurar Variables de Entorno

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

#### 3. Levantar Servicios con Docker

```bash
# Levantar todos los servicios
docker-compose -f infrastructure/docker-compose.yml up --build

# O levantar servicios específicos
docker-compose -f infrastructure/docker-compose.yml up postgres redis
```

#### 4. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
alembic upgrade head

# Ejecutar aplicación
python -m src.main
```

#### 5. Configurar Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev
```

## Estructura del Proyecto

```
auto-grader/
├── backend/
│   ├── src/
│   │   ├── auth/              # Autenticación y autorización
│   │   ├── config/            # Configuraciones
│   │   ├── database/          # Modelos y configuración de BD
│   │   ├── models/            # Modelos de negocio
│   │   ├── routes/            # Endpoints de la API
│   │   ├── services/          # Lógica de negocio
│   │   └── utils/             # Utilidades
│   ├── migrations/            # Migraciones de base de datos
│   ├── tests/                 # Tests unitarios
│   └── requirements.txt       # Dependencias Python
├── frontend/
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   ├── pages/            # Páginas de la aplicación
│   │   ├── services/         # Servicios de API
│   │   └── utils/            # Utilidades
│   └── package.json          # Dependencias Node.js
├── infrastructure/
│   └── docker-compose.yml    # Configuración de servicios
└── docs/                     # Documentación
```

## Comandos de Desarrollo

### Backend

```bash
# Ejecutar tests
pytest

# Ejecutar tests con cobertura
pytest --cov=src

# Crear migración
alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar migraciones
alembic upgrade head

# Revertir migración
alembic downgrade -1

# Linter
flake8 src/
black src/
```

### Frontend

```bash
# Desarrollo
npm run dev

# Build para producción
npm run build

# Tests
npm test

# Linter
npm run lint

# Preview de build
npm run preview
```

### Docker

```bash
# Levantar servicios
docker-compose -f infrastructure/docker-compose.yml up

# Levantar en background
docker-compose -f infrastructure/docker-compose.yml up -d

# Ver logs
docker-compose -f infrastructure/docker-compose.yml logs -f

# Parar servicios
docker-compose -f infrastructure/docker-compose.yml down

# Rebuild
docker-compose -f infrastructure/docker-compose.yml up --build
```

## Flujo de Trabajo

### 1. Desarrollo de Features

1. Crear rama desde `main`
   ```bash
   git checkout -b feature/nombre-feature
   ```

2. Desarrollar feature
3. Ejecutar tests
4. Crear pull request

### 2. Manejo de Base de Datos

1. Modificar modelos en `src/database/models.py`
2. Crear migración
   ```bash
   alembic revision --autogenerate -m "Descripción"
   ```
3. Revisar migración generada
4. Aplicar migración
   ```bash
   alembic upgrade head
   ```

### 3. Testing

#### Tests Unitarios
- Ubicación: `backend/tests/`
- Ejecutar: `pytest`
- Cobertura: `pytest --cov=src`

#### Tests de Integración
- Probar endpoints completos
- Validar flujos de usuario
- Verificar integración con base de datos

## Convenciones de Código

### Python

- **PEP 8**: Seguir estándares de Python
- **Type Hints**: Usar anotaciones de tipo
- **Docstrings**: Documentar funciones y clases
- **Naming**: snake_case para variables y funciones

```python
def process_assignment(assignment_id: str) -> CorrectionResult:
    """
    Procesar una tarea y generar corrección.
    
    Args:
        assignment_id: ID de la tarea a procesar
        
    Returns:
        CorrectionResult: Resultado de la corrección
        
    Raises:
        ValueError: Si la tarea no existe
    """
    pass
```

### TypeScript/React

- **ESLint**: Seguir reglas de ESLint
- **Prettier**: Formateo automático
- **Naming**: camelCase para variables, PascalCase para componentes
- **Props Interface**: Definir interfaces para props

```typescript
interface AssignmentProps {
  assignmentId: string;
  onComplete: (result: CorrectionResult) => void;
}

const AssignmentComponent: React.FC<AssignmentProps> = ({ 
  assignmentId, 
  onComplete 
}) => {
  // Component logic
};
```

## Debugging

### Backend

```python
# Usar logging
import logging
logger = logging.getLogger(__name__)

logger.info("Procesando tarea")
logger.error(f"Error: {error}")
```

### Frontend

```typescript
// Usar console.log para debugging
console.log('Debug info:', data);

// React DevTools para inspeccionar componentes
```

### Base de Datos

```bash
# Conectar a PostgreSQL
docker exec -it autograder_postgres psql -U autograder_user -d autograder

# Ver tablas
\dt

# Ver estructura de tabla
\d users
```

## Troubleshooting

### Problemas Comunes

#### 1. Error de Conexión a Base de Datos
```bash
# Verificar que PostgreSQL esté corriendo
docker-compose -f infrastructure/docker-compose.yml ps

# Ver logs de PostgreSQL
docker-compose -f infrastructure/docker-compose.yml logs postgres
```

#### 2. Error de Dependencias
```bash
# Limpiar cache de pip
pip cache purge

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

#### 3. Error de Migraciones
```bash
# Ver estado de migraciones
alembic current

# Ver historial
alembic history

# Resetear migraciones (¡CUIDADO!)
alembic stamp head
```

#### 4. Error de Ollama
```bash
# Verificar que Ollama esté corriendo
docker-compose -f infrastructure/docker-compose.yml logs ollama

# Reiniciar Ollama
docker-compose -f infrastructure/docker-compose.yml restart ollama
```

## Performance

### Optimizaciones de Backend

1. **Queries de Base de Datos**
   - Usar índices apropiados
   - Evitar N+1 queries
   - Usar eager loading cuando sea necesario

2. **Cache**
   - Implementar cache Redis
   - Cache de respuestas de IA
   - Cache de datos de configuración

3. **Procesamiento Asíncrono**
   - Usar colas para tareas largas
   - Procesamiento en paralelo
   - Timeout y retry logic

### Optimizaciones de Frontend

1. **Bundle Size**
   - Code splitting
   - Lazy loading de componentes
   - Tree shaking

2. **Rendering**
   - Memoización de componentes
   - Virtualización de listas largas
   - Optimización de re-renders

## Seguridad

### Desarrollo

1. **Variables de Entorno**
   - Nunca commitear archivos `.env`
   - Usar valores seguros en producción
   - Rotar claves regularmente

2. **Validación de Entrada**
   - Validar todos los inputs
   - Sanitizar datos de usuario
   - Usar CSRF tokens

3. **Autenticación**
   - JWT tokens seguros
   - Refresh tokens
   - Rate limiting

## Contribución

### Proceso de Contribución

1. Fork del repositorio
2. Crear rama de feature
3. Desarrollar y testear
4. Crear pull request
5. Code review
6. Merge a main

### Code Review

- Revisar lógica de negocio
- Verificar tests
- Validar seguridad
- Comprobar performance
- Revisar documentación

## Recursos Adicionales

- [Documentación de Flask](https://flask.palletsprojects.com/)
- [Documentación de React](https://reactjs.org/docs/)
- [Documentación de SQLAlchemy](https://docs.sqlalchemy.org/)
- [Documentación de Docker](https://docs.docker.com/)
- [Guía de Git](https://git-scm.com/docs)
