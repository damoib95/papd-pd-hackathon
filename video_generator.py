import os
import logging
from dotenv import load_dotenv
from gtts import gTTS
from moviepy.editor import *
from PIL import Image
import json
import os
from pydub import AudioSegment

logging.basicConfig(level=logging.INFO)

def load_json(filename):
    json_path = os.path.join('data', 'output', f'{filename}.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)['slides']
    except FileNotFoundError as e:
        logging.error(f"El archivo {json_path} no fue encontrado.")
        raise e
    except json.JSONDecodeError as e:
        logging.error(f"No se pudo decodificar el archivo JSON {json_path}.")
        raise e

def create_text_clip(text, duration, pos=("left", "top"), fontsize=40, color='white', font="Arial", max_width=720, align='center'):
    clip = TextClip(text, fontsize=fontsize, color=color, font=font, method='caption', size=(max_width, None), align=align)
    clip = clip.set_duration(duration).set_position(pos).fadein(1).fadeout(1)
    return clip

def create_slide(slide, size, index):
    slide_text = slide.get("audio", "")
    tts = gTTS(text=slide_text, lang='en', tld='co.uk')
    tmp_audio_path = os.path.join('data', 'tmp', f'temp_audio_{index}.mp3')
    tts.save(tmp_audio_path)
    
    audio_clip = AudioFileClip(tmp_audio_path)

    background_clip = ColorClip(size=size, color=(255, 255, 255)).set_duration(audio_clip.duration)

    title_clip = create_text_clip(
        text=slide["title"],
        duration=audio_clip.duration,
        pos=("center", 50),
        fontsize=48,
        color='black',
        font="Georgia-Bold",
        max_width=size[0]*0.8
    )

    bullets_clip = create_text_clip(
        text='\n'.join(f'• {line}' for line in slide["info"]),
        duration=audio_clip.duration,
        pos=(50, 200),
        fontsize=32,
        color='black',
        font="Arial",
        max_width=size[0]*0.8,
        align='West'
    )
    
    elements = [background_clip, title_clip, bullets_clip]
    slide_clip = CompositeVideoClip(elements)
    slide_clip = slide_clip.set_audio(audio_clip)

    return slide_clip, tmp_audio_path

def create_video(filename, size=(1280, 720)):
    slides = load_json(filename)
    clips = []
    tmp_audio_paths = []

    for index, slide in enumerate(slides):
        slide_clip, tmp_audio_path = create_slide(slide, size, index)
        clips.append(slide_clip)
        tmp_audio_paths.append(tmp_audio_path)

    final_video = concatenate_videoclips(clips, method="compose")
    output_path = os.path.join('data', 'output', f'{filename}.mp4')
    tmp_audio_path = os.path.join('data', 'tmp', 'temp_audio.m4a')
    final_video.write_videofile(output_path, fps=12, audio_codec='aac', temp_audiofile=tmp_audio_path, remove_temp=True)

def script_to_video():
    logging.info(f'Iniciando generación de vídeo')
    filename = os.getenv("FILENAME")
    create_video(filename, size=(1280, 720))
    logging.info('Limpiando archivos temporales')
    for path in tmp_audio_paths:
        os.remove(path)
