from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..' )))
from lib.utils.debounce.main import Debounce
from lib.utils.debounce.user_data import user_messages
from lib.evolution.routes.main import Evolution
from lib.evolution.webhook.main import process_webhook
from threading import Thread

app = Flask(__name__)

class InputData(BaseModel):
    input: str
    memoryKey: str
    remoteJid: str
    messageType: str

@app.route('/')
def home_page():
    return '<h1>Hello, World!</h1>'

@app.route('/api/chat', methods=['POST'])
def webhook():
    try:
        data = request.json
        data = InputData(**process_webhook(data))

        user_input = data.input
        memory_key = data.memoryKey
        remote_jid = data.remoteJid

        if memory_key in user_messages:
            user_messages[memory_key].append(user_input)
        else:
            user_messages[memory_key] = [user_input]

        def debounce_handler():
            wpp = Evolution(api_key=os.getenv("EVOLUTION_API_KEY"), instance=os.getenv("EVOLUTION_INSTANCE_NAME"))
            debounce = Debounce(callback=wpp.send_text_handler(remote_jid=remote_jid, memory_key=memory_key), interval=5.0)
            debounce.call(memory_key)

        thread = Thread(target=debounce_handler)
        thread.start()

        return jsonify({'status': 'success'})

    except ValidationError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
