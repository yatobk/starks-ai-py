import requests
from random import randint
from lib.utils.debounce.user_data import user_messages
from lib.langchain.agents.OpenAiAgent import answer
import os

class Evolution:
    def __init__(self, instance: str, api_key: str):
        self.base_url = os.getenv("EVOLUTION_BASE_URL")
        self.instance = instance
        self.api_key = api_key

    def send_text(self, remote_jid: str, text: str):
        headers = {
            "apiKey": self.api_key
        }

        payload = {
            "number": remote_jid,
            "options": {
                "delay": randint(1200, 2000),
                "presence": "composing",
                "linkPreview": True
            },
            "textMessage": {
                "text": text
            }
        }

        response = requests.post(
            f"{self.base_url}/message/sendText/{self.instance}", 
                json=payload, headers=headers
            )
        
        return response.json()
    

    def send_text_handler(self, memory_key, remote_jid):
        if memory_key in user_messages:
            messages = '\n\n'.join(user_messages[memory_key])
            message = answer(userInput=messages, memoryKey=memory_key)
            del user_messages[memory_key]
            for m in message:
                self.send_text(remote_jid=remote_jid, text=m["message"])

    def convert_audio_to_base_64(self, audio_id):
        headers = {
            "apiKey": self.api_key
        }
        
        payload = {
            "message": {
                "key": {
                    "id": audio_id
                }
            },
            "convertToMp4": False
        }

        response = requests.post(
            f"{self.base_url}/chat/getBase64FromMediaMessage/{self.instance}", 
                json=payload, headers=headers
            )
        base_64 = response.json()["base64"]

        return base_64
