# =============================================================
# BROKEN TUNES — Backend Dockerfile
# Imagen base: python:3.12-slim (lightweight)
# =============================================================

FROM python:3.12-slim

# Evita que Python genere archivos .pyc y bufferiza stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema necesarias para mysql-connector
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python primero (aprovecha cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]