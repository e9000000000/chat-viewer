from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
from time import sleep
import webbrowser
import json
import asyncio

from chats import ChatUnifer, ErrorMessage, twitch
from config import HOST, PORT, TWITCH_CHANNEL
from utils import change_config_variable


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


@app.route('/')
def index():
    return render_template('index.html', host=HOST, port=PORT)

@app.route('/settings/', methods=['GET', 'POST'])
def settings():
    global TWITCH_CHANNEL
    if request.method == 'POST':
        TWITCH_CHANNEL = request.form['twitch_chan']
        change_config_variable('TWITCH_CHANNEL', f'\'{TWITCH_CHANNEL}\'')

    return render_template('settings.html', current_twitch=TWITCH_CHANNEL)

@socketio.on('message')
def sock_send(message:str):
    if message == 'START':
        chat = ChatUnifer()

        if TWITCH_CHANNEL != '':
            twitch_chat = twitch.AnonimTwitchChat(TWITCH_CHANNEL)
            chat.add_chat(twitch_chat)

        for message in chat.listen():
            if type(message) is ErrorMessage:
                msg_dict = {
                    'error': message.text
                }
            else:
                msg_dict = {
                    'text': message.text,
                    'author': message.author
                }
            send(json.dumps(msg_dict))





if __name__ == '__main__':
    app.env = 'development'
    if TWITCH_CHANNEL == '':
        webbrowser.open(f'http://{HOST}:{PORT}/settings')
    socketio.run(app, host=HOST, port=PORT)