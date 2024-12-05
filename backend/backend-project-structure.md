```
backend/
│
├── src/
│   ├── __init__.py
│   ├── main.py               # Punto de entrada principal
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py       # Configuraciones de la aplicación
│   │   └── logging.py        # Configuración de logging
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── assignment.py     # Modelo de datos para tareas
│   │   └── correction.py     # Modelo de corrección
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── correction_service.py     # Servicio principal de corrección
│   │   └── ollama_service.py         # Interacción con Ollama
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_handler.py   # Manejo de archivos
│   │   └── validators.py     # Validaciones
│   │
│   └── routes/
│       ├── __init__.py
│       └── assignment_routes.py  # Rutas de la API
│
├── tests/
│   ├── __init__.py
│   ├── test_correction_service.py
│   ├── test_file_handler.py
│   └── test_routes.py
│
├── requirements.txt
├── Dockerfile
└── README.md
```
