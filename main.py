import os
import logging
from dotenv import load_dotenv
from data_extraction import video_to_text

logging.basicConfig(level=logging.INFO)

def main():
    logging.info('Hello, world!')
    load_dotenv()
    format = os.getenv("FORMAT")
    if format in 'mp4':
        video_to_text()


if __name__ == "__main__":
    main()
