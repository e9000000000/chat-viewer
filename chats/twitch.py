import asyncio
import websockets
import random
import re

from . import Chat, ChatMessage

class TwitchError(Exception):
    def __init__(self, text):
        self.txt = text

class AnonimTwitchChat(Chat):
    def __init__(self, channel:str):
        self.__channel = channel
        self.__user = f'justinfan{random.randrange(10000, 99999)}'
        self.__irc = 'SCHMOOPIIE'
        self.__web_socket = None

        super().__init__()

    def __check_if_ping(self, responce):
        if responce == 'PING :tmi.twitch.tv\r\n':
            return True
        return False

    def __check_if_PRIVMSG(self, responce):
        if 'PRIVMSG #' in responce:
            return True
        return False

    def __check_if_commands(self, responce):
        if ':tmi.twitch.tv CAP * ACK :twitch.tv/tags twitch.tv/commands\r\n' == responce:
            return True
        return False
        
    def __check_if_Wellcome(self, responce):
        if re.match(r':tmi\.twitch\.tv 001 .* :Welcome, GLHF!', responce) is not None:
            return True
        return False

    def __check_if_JOIN(self, responce):
        if re.match(r':.*!.*@.*.tmi.twitch.tv JOIN #.*', responce) is not None:
            return True
        return False


    async def connect(self):
        self.__web_socket = await websockets.connect('wss://irc-ws-r.chat.twitch.tv/').__aenter__()
        await self.__web_socket.send('CAP REQ :twitch.tv/tags twitch.tv/commands')
        await self.__web_socket.send(f'PASS {self.__irc}')
        await self.__web_socket.send(f'NICK {self.__user}')
        await self.__web_socket.send(f'USER {self.__user} 8 * :{self.__user}')

        responce = await self.__web_socket.recv()
        if not self.__check_if_commands(responce):
            raise TwitchError('Twitch connection error')

        responce = await self.__web_socket.recv()
        if not self.__check_if_Wellcome(responce):
            raise TwitchError('Twitch connection error')

        await self.__web_socket.send(f'JOIN #{self.__channel}')
        responce = await self.__web_socket.recv()
        if not self.__check_if_JOIN(responce):
            raise TwitchError('Twitch channel join error')

        self.__is_connected = True

    async def disconnect(self):
        self.__web_socket.close()
        self.__is_connected = False

    async def listen(self):
        if not self.__is_connected:
            raise TwitchError('Twitch is not connected')

        while 1:
            responce = await self.__web_socket.recv()

            if responce == '':
                raise TwitchError('Twitch has been disconnected')

            if self.__check_if_ping(responce):
                await self.__web_socket.send('PONG')
                continue
            
            if self.__check_if_PRIVMSG(responce):
                author = re.search(r'(?<=display-name=)[^\;]*', responce).group(0)
                message = re.search(r'(?<=PRIVMSG #).*', responce).group(0)
                message = re.search(r'(?<= :).*', message).group(0)

                yield ChatMessage(message, author, 'twitch')

    async def send_message(self, msg_text):
        if not self.__is_connected:
            raise TwitchError('Twitch no account to send message')
    
