# Imagen base de Python
FROM python:3.10-slim-buster

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Ollama
RUN curl https://ollama.ai/install.sh | sh

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Variables de entorno
ENV FLASK_APP=src/main.py
ENV FLASK_ENV=production

# Exponer puerto
EXPOSE 5000

# Comando de inicio
CMD ["flask", "run", "--host=0.0.0.0"]