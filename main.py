import os
import logging
from dotenv import load_dotenv
from data_extraction import video_to_text
from text_structure import text_to_script
from video_generator import script_to_video


logging.basicConfig(level=logging.INFO)

def main():
    logging.info('Hello, world!')
    load_dotenv()
    format = os.getenv("FORMAT")
    if format in 'mp4':
        video_to_text()
    text_to_script()
    script_to_video()


if __name__ == "__main__":
    main()
