import os
import logging
from pydub import AudioSegment
import whisper
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

def video_to_text():
    logging.info(f'Iniciando conversión de vídeo a texto')
    filename = os.getenv("FILENAME")
    format = os.getenv("FORMAT")
    video_path = os.path.join('data', 'input', f'{filename}.{format}')
    logging.info(f'Abriendo archivo {video_path}')
    video = AudioSegment.from_file(video_path, format=format)
    audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)

    audio_path = os.path.join('data', 'output', f"{filename}_tmp.mp3")
    logging.info(f'Exportando audio {audio_path}')
    audio.export(audio_path, format="mp3")

    language = os.getenv("LANGUAGE")
    model = whisper.load_model("base")
    logging.info('Generando transcripción de audio')
    result = model.transcribe(audio_path, language=language, fp16=False)

    text_path = os.path.join('data', 'output', f"{filename}.txt")
    with open(text_path, "w") as file:
        file.write(result["text"])

    logging.info('Limpiando archivos temporales')
    os.remove(audio_path)        

    

    