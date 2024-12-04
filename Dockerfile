# Imagen base de Python
FROM python:3.11.5-slim

# Determinamos nuestro directorio de trabajo
WORKDIR /app

# Dependencias y librerías del sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    g++ \
    python3-dev \
    imagemagick \
    build-essential \
    && apt-get clean

# Copia el archivo de requirements
COPY requirements.txt /app/requirements.txt

# Instalar las dependencias de Python
RUN python -m pip install --upgrade pip

# Instalar las demás dependencias
RUN pip install --no-cache-dir -r requirements.txt 

# Descargar modelo de SpaCy
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download es_core_news_sm

# Descargar y cachear el modelo de Whisper si es necesario
COPY models/tiny.pt /root/.cache/whisper/tiny.pt

# Reemplazar el archivo policy.xml
COPY policy.xml /etc/ImageMagick-6/policy.xml

# Agregamos nuestros archivos
COPY . /app

# Exponer el puerto para la API
EXPOSE 8000

# Comando por defecto
CMD ["python", "main.py"]
