from lib.utils.ai.transcriptAudio import transcribe_audio
from lib.utils.ai.describeImage import describe_image
from lib.evolution.routes.main import Evolution

def process_webhook(event: dict):
    payload = event["body"]
    event_type = payload["event"]

    if event_type == "messages.upsert":
        message_type = payload["data"]["messageType"]
        match message_type:
            case "extendedTextMessage":
                return get_extended_message(event)
            case "ephemeralMessage":
                return get_extended_message(event)
            case "conversation":
                return get_conversation_message(event)
            case "audioMessage":
                return get_audio_message(event)
            case "imageMessage":
                return get_image_message(event)
            case _:
                return send_error_message(event)

def send_error_message(event):
    payload = event["body"]
    remote_jid = payload["data"]["key"]["remoteJid"]
    message_type = payload["data"]["messageType"]
    user = payload["sender"]
    text = "Desculpe mas não entendi sua última mensagem, poderia mandar em texto por favor?"
    return response_handler(remote_jid=remote_jid, text=text, message_type=message_type, user=user)

def response_handler(remote_jid, text, message_type, user):
    data = {
        "messageType": message_type,
        "input": text,
        "remoteJid": remote_jid,
        "memoryKey": user + "@" + remote_jid
    }
    return data

def get_conversation_message(event):
    payload = event["body"]
    remote_jid = payload["data"]["key"]["remoteJid"]
    text = payload["data"]["message"]["conversation"]
    message_type = payload["data"]["messageType"]
    user = payload["sender"]
    return response_handler(remote_jid=remote_jid, text=text, message_type=message_type, user=user)

def get_extended_message(event):
    payload = event["body"]
    remote_jid = payload["data"]["key"]["remoteJid"]
    text = payload["data"]["message"]["extendedTextMessage"]["text"]
    message_type = payload["data"]["messageType"]
    user = payload["sender"]
    
    return response_handler(remote_jid=remote_jid, text=text, message_type=message_type, user=user)

def get_audio_message(event):
    payload = event["body"]
    remote_jid = payload["data"]["key"]["remoteJid"]
    message_type = payload["data"]["messageType"]
    user = payload["sender"]
    audio_id = payload["data"]["key"]["id"]
    instance = payload["data"]["owner"]
    api_key = payload["apikey"]    

    wpp = Evolution(api_key=api_key, instance=instance)

    audio_base_64 = wpp.convert_audio_to_base_64(audio_id)
    text = transcribe_audio(audio_base_64)["responseText"]
    transcription = response_handler(remote_jid=remote_jid, text=text, message_type=message_type, user=user)
    return transcription

def get_image_message(event):
    payload = event["body"]
    remote_jid = payload["data"]["key"]["remoteJid"]
    image_base_64 = payload["data"]["message"]["base64"]
    message_type = payload["data"]["messageType"]
    user = payload["sender"]
    text = describe_image(image_base_64)["responseText"]

    try: 
        captions = payload["data"]["message"]["ImageMessage"]["caption"]
        caption = f"{captions}\n\n"
    except:
        caption = ""

    text = caption + text

    transcription = response_handler(remote_jid=remote_jid, text=text, message_type=message_type, user=user)

    return transcription
       