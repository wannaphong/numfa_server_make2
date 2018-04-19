# -*- coding: utf-8 -*-
from flask import Flask, render_template,request, jsonify
from run import get_chatbot

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat_message')
def get_bot_response():
    userText = request.args.get('msg')
    return str(get_chatbot(userText))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081)