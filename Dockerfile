# Imagen base de Python
FROM python:3.10-slim

# Determinamos nuestro directorio de trabajo
WORKDIR /app

# Dependencias y librerias
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    python3-dev \
    imagemagick \
    && apt-get clean

# Reemplazar el archivo policy.xml
COPY policy.xml /etc/ImageMagick-6/policy.xml

# Agregamos nuestros archivos
COPY . /app

# Instalar requirements
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Como se ejecuta
EXPOSE 8000

CMD ["python", "main.py"]

