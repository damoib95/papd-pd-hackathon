import os
import logging
from dotenv import load_dotenv
from data_extraction import video_to_text
from text_structure import text_to_script
from video_generator import script_to_video
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p')

def main():
    logging.info('CoreClip 1.0.0')
    load_dotenv()
    format = os.getenv("FORMAT")
    if format in 'mp4':
        video_to_text()
    text_to_script()
    script_to_video()


if __name__ == "__main__":
    main()
