import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

def text_to_script():
    logging.info(f'Iniciando resumen y generación de guión')
    filename = os.getenv("FILENAME")
