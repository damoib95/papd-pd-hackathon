import os
import logging
from dotenv import load_dotenv
import spacy
import json
from transformers import pipeline
from collections import Counter

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p')

def split_text(text, max_words=700):
    words = text.split()
    return [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

def generate_summary(text, summarizer, max_length, min_length):
    return summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']

def extract_bullets(refined_audio_summary, nlp_model, max_length=50):
    doc = nlp_model(refined_audio_summary)
    
    sentences = [sent.text.strip() for sent in doc.sents]
    
    if len(sentences) == 1:
        sentences = refined_audio_summary.split('"')
        sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) == 1:
        words = refined_audio_summary.split()
        sentences = [' '.join(words[i:i + max_length]) for i in range(0, len(words), max_length)]
    
    return sentences

def extract_keywords(text, nlp_model, max_keywords=3):
    doc = nlp_model(text)
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2]
    most_common = Counter(keywords).most_common(max_keywords)
    return [kw[0] for kw in most_common]

def generate_title_with_keywords(text, nlp_model, max_keywords=3):
    keywords = extract_keywords(text, nlp_model, max_keywords=max_keywords)
    return " ".join(keywords).title()

def text_to_script():
    logging.info(f'Iniciando resumen y generación de guión')

    language = os.getenv("LANGUAGE")
    if language=='english':
        nlp = spacy.load("en_core_web_sm")
    elif language=='spanish':
        nlp = spacy.load("es_core_news_sm")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    filename = os.getenv("FILENAME")
    text_path = os.path.join('data', 'output', f'{filename}.txt')
    try:
        with open(text_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        logging.error(f"El archivo {text_path} no fue encontrado.")
        return ""
    except Exception as e:
        logging.error(f"Ocurrió un error al leer el archivo: {e}")
        return ""

    slides = []
    language = os.getenv("LANGUAGE")
    if language=='spanish':
        max_words = 400
    elif language=='english':
        max_words = 700
    chunks = split_text(text, max_words)

    for i, chunk in enumerate(chunks, start=1):
        audio_summary = generate_summary(chunk, summarizer, max_length=150, min_length=100)

        refined_audio_summary = generate_summary(audio_summary, summarizer, max_length=75, min_length=50)
        bullet_points = extract_bullets(refined_audio_summary, nlp)

        title = generate_title_with_keywords(chunk, nlp, max_keywords=3)

        slides.append({
            "title": title,
            "info": bullet_points,
            "audio": audio_summary
        })

    data =  {"slides": slides}

    json_path = os.path.join('data', 'output', f'{filename}.json')
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logging.info(f"Exportación de JSON {filename}")
    
