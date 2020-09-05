import asyncio
import websockets
import random
import re

from . import Chat, Message

class TwitchChat(Chat):
    def __init__(self, channel):
        self.__channel = channel

    def __check_if_ping(self, responce):
        if responce is None:
            return False

        if responce == 'PING :tmi.twitch.tv\r\n':
            return True
        return False

    def __check_if_PRIVMSG(self, responce):
        if responce is None:
            return False

        if 'PRIVMSG #' in responce:
            return True
        return False

    async def connect(self):
        pass

    async def listen(self):
        username = f'justinfan{random.randrange(10000, 99999)}'

        async with websockets.connect('wss://irc-ws-r.chat.twitch.tv/') as websocket:
            await websocket.send('CAP REQ :twitch.tv/tags twitch.tv/commands')
            await websocket.send('PASS SCHMOOPIIE')
            await websocket.send(f'NICK {username}')
            await websocket.send(f'USER {username} 8 * :{username}')
            await websocket.send(f'JOIN #{self.__channel}')
            
            while 1:
                responce = await websocket.recv()

                if self.__check_if_ping(responce):
                    await websocket.send('PONG')
                    continue
                
                if self.__check_if_PRIVMSG(responce):
                    author = re.search(r'(?<=display-name=)[^\;]*', responce).group(0)
                    message = re.search(r'(?<=PRIVMSG #).*', responce).group(0)
                    message = re.search(r'(?<= :).*', message).group(0)

                    yield f'{author}:{message}'

    async def send_message(self, msg_text):
        pass
