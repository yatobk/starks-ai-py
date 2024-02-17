from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..' )))

from lib.langchain.agents.OpenAiAgent import answer

app = Flask(__name__)

class InputData(BaseModel):
    input: str
    memoryKey: str

@app.route('/')
def homePage():
    return '<h1>Hello, World!</h1>'

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = InputData(**request.json)
        
        user_input = data.input
        memory_key = data.memoryKey

        Ai_answer = answer(userInput=user_input, memoryKey=memory_key)
        
        return jsonify({ 'status': 'success', 'text': Ai_answer })
    
    except ValidationError as e:
        return jsonify( {'status': 'error', 'message': str(e)} ), 400
