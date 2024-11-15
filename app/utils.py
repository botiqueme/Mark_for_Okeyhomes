from datetime import datetime
from fuzzywuzzy import fuzz
import os
from flask import Response
import re
from pydub import AudioSegment
import uuid
from collections import defaultdict
import re


def remove_keywords(message):
    similarity = fuzz.token_set_ratio(message.lower(), os.getenv("KEYWORD_DELETE").lower())
    if similarity >= float(os.environ.get('KEYWORD_SIMILARITY_THRESHOLD')):
        # Se la somiglianza è sopra la soglia, rimuovi la parola chiave
        message = message.replace(str(os.getenv('KEYWORD_DELETE')), '')
    if message:
        return message
    else:
        return None

def check_trigger_functions(message):
    appontment_keyword = os.getenv("KEYWORD_APPOINTMENT")

    similarity = fuzz.ratio(message.lower(), appontment_keyword.lower())

    if similarity >= float(os.environ.get('KEYWORD_SIMILARITY_THRESHOLD')) or appontment_keyword.lower() in message.lower():
        message = re.sub(appontment_keyword, '', message, flags=re.IGNORECASE)
        # Se la somiglianza è sopra la soglia, chiama la funzione
        return ("take_appointment", message)
    else:
        return (False, message)

def text_to_html(text):
    # Sostituisce "**<testo>**" con "<b><testo></b>"
    return re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)

def get_apointment():
    now = datetime.datetime.now()
    appointment_time = now + datetime.timedelta(minutes=30)

    # Controlla se è troppo tardi in giornata
    if now.hour >= 17:
        appointment_time += datetime.timedelta(days=1)
        appointment_time = appointment_time.replace(hour=10, minute=0, second=0, microsecond=0)

    # Controlla il giorno della settimana (5 = sabato, 6 = domenica)
    while appointment_time.weekday() in [5, 6]:
        appointment_time += datetime.timedelta(days=1)
        appointment_time = appointment_time.replace(hour=10, minute=0, second=0, microsecond=0)

    return appointment_time

def transcribe(openai_client, audio_file):
    unique_filename = str(uuid.uuid4())

    audio_data = AudioSegment.from_file_using_temporary_files(audio_file)
    temp_filename = f"./static/tmp_audio/{unique_filename}.mp3"
    audio_data.export(temp_filename, format='mp3')

    with open(temp_filename, 'rb') as f:
        message = openai_client.speech_to_text(f)

    os.remove(temp_filename)

    return message


def clean_tmp():
    tmp_folder = './static/tmp_audio'
    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)
    for file in os.listdir('./static/tmp_audio'):
        os.remove(f'./static/tmp_audio/{file}')


def log_conversation(logger, thread_id, user_input, bot_response):
    logger.info(f"##{thread_id}## | User: {user_input} - Bot: {bot_response}")


def parse_log_file():
    conversations = defaultdict(list)
    total_messages = 0
    thread_dates = {}  # Dizionario per memorizzare la data di inizio di ciascun thread

    with open('./logs/chatbot.log', 'r') as file:
        for line in file:
            # match = re.search(r'##(thread_[\w\d]+)## \| User: (.*?) - Bot: (.*)', line)
            match = re.search(r'(\d{4}-\d{2}-\d{2}) \d{2}:\d{2}:\d{2},\d{3}:##(thread_[\w\d]+)## \| User: (.*?) - Bot: (.*)', line)

            if match:
                date_str, thread_id, user_msg, bot_msg = match.groups()
                if thread_id not in thread_dates:
                    thread_dates[thread_id] = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')

                conversations[thread_id].append((user_msg, bot_msg))
                total_messages += 2  # Conta sia il messaggio dell'utente che la risposta del bot

    # Calcola altre statistiche
    num_conversations = len(conversations)
    avg_messages_per_conversation = total_messages / num_conversations if num_conversations > 0 else 0
    longest_conversation = max(conversations.values(), key=len, default=[])
    shortest_conversation = min(conversations.values(), key=len, default=[])

    return {
        "total_messages": total_messages,
        "num_conversations": num_conversations,
        "avg_messages_per_conversation": avg_messages_per_conversation,
        "longest_conversation": len(longest_conversation),
        "shortest_conversation": len(shortest_conversation),
        "conversations": conversations,
        "thread_dates": thread_dates  # Aggiungi le date dei thread
    }
