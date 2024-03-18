import os
import base64
import random
import string
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

def transcribe_audio(base64_audio):
    client = OpenAI()
    audio_data = base64.b64decode(base64_audio)
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    audio_file_name = f"audio_{random_string}.ogg"
    tmp_folder = "tmp" 
    tmp_path = os.path.join(os.getcwd(), tmp_folder)
    audio_file_path = os.path.join(tmp_path, audio_file_name)

    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    with open(audio_file_path, 'wb') as audio_file:
        audio_file.write(audio_data)

    try:    
        audio_file= open(audio_file_path, "rb")
        transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        language="pt",
        response_format="text"
        )

        os.remove(audio_file_path)

        return { "responseText": transcription, "totalTokens": 0 }

    except Exception as error:
        print("Erro na transcrição:", error)
        raise error
