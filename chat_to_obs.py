from flask import Flask, render_template
from flask_socketio import SocketIO, send
from time import sleep

from chats import ChatListener, twitch
from config import HOST, PORT, TWITCH_CHANNEL


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


@app.route('/')
def index():
    return render_template('index.html', host=HOST, port=PORT)

@socketio.on('message')
def sock_send(message:str):
    if message == 'START':
        chat = ChatListener()

        if TWITCH_CHANNEL != '':
            twitch_chat = twitch.Chat(TWITCH_CHANNEL)
            chat.add_chat(twitch_chat)

        for message in chat.listen():
            print(message)
            send(message)





if __name__ == '__main__':
    app.env = 'development'
    socketio.run(app, host=HOST, port=PORT)