import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

def script_to_video():
    logging.info(f'Iniciando generación de vídeo')
    filename = os.getenv("FILENAME")