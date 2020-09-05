import asyncio
from threading import Thread
from time import sleep
from datetime import datetime
from abc import ABCMeta, abstractmethod

class Message():
    """message text and some additional information"""

    def __init__(self, text:str='', author:str='', platform:str='', receiving_datetime:datetime=datetime.now()):
        self.text = text
        self.author = author
        self.platform = platform
        self.receiving_datetime = receiving_datetime

class Chat(metaclass=ABCMeta):
    """
    Chat\n

    first of all u should use self.connect().\n
    if connect is success u can send messages and listen for messages\n
    """

    @abstractmethod
    async def connect(self) -> None:
        """will connect to some service"""
        pass

    @abstractmethod
    async def listen(self) -> Message:
        """will receive messages and yield it"""
    
    @abstractmethod
    async def send_message(self, msg_text) -> None:
        """will send message to the chat"""
        pass
        
class ChatUnifer():
    """ChatUnifer\n
    unites chats to one\n\n
    """
    __doc__ += Chat.__doc__

    def __init__(self, *chats):
        self.__chats = []
        self.__messages = []

        for chat in chats:
            self.add_chat(chat)

    async def __save_message(self, chat):
        async for message in chat.listen():
            self.__messages.append(message)

    def add_chat(self, chat):
        """added chat to chat list, chat should be subclass of \"Chat\" """
        if issubclass(type(chat), Chat):
            self.__chats.append(chat)
        else:
            raise TypeError('object should be subclass of "Chat"')

    def connect(self):
        """connect all chats"""
        for chat in self.__chats:
            asyncio.run(chat.connect())

    def listen(self):
        """listen for a messages from all chats"""
        for chat in self.__chats:
            Thread(target=asyncio.run, args=(self.__save_message(chat), ), daemon=True).start()

        while 1:
            if self.__messages.__len__() > 0:
                yield self.__messages.pop()
            else:
                sleep(0.1)

    def send_message(self, msg_text):
        """send message to all chats"""
        for chat in self.__chats:
            asyncio.run(chat.send_message(msg_text))
