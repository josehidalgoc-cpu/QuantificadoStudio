FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN pip install --no-cache-dir pandas matplotlib seaborn openpyxl

# Copiar el script y los datos
COPY . /app

# Comando por defecto para correr el análisis
CMD ["python", "analisis_canasta.py"]