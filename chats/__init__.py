import asyncio
from threading import Thread
from time import sleep
from datetime import datetime

class Message():
    def __init__(self, text:str=''):
        self.text = text

class ChatMessage(Message):
    """message text and some additional information"""

    def __init__(self, text:str='', author:str='', platform:str='', receiving_datetime:datetime=datetime.now()):
        super().__init__(text)
        self.author = author
        self.platform = platform
        self.receiving_datetime = receiving_datetime

class ErrorMessage(Message):
    """"""

class Chat():
    """
    Chat\n

    first of all u should use self.connect().\n
    if connect is success u can send messages and listen for messages\n
    """
    def __init__(self):
        self.__is_connected = False

    async def connect(self) -> None:
        """connect and become enabled to use"""
        pass

    async def disconnect(self) -> None:
        """disconnect and become disabled to use"""
        pass

    async def listen(self) -> ChatMessage:
        """receive messages and yield it"""
        pass

    async def send_message(self, msg_text) -> None:
        """send message to the chat"""
        pass

    def is_connected(self): return self.__is_connected
        
class ChatUnifer():
    """ChatUnifer\n
    unites chats to one
    """

    def __init__(self, *chats):
        self.__chats = []
        self.__messages = []

        for chat in chats:
            self.add_chat(chat)

    async def __save_messages(self, chat):
        try:
            if not chat.is_connected():
                await chat.connect()

            async for message in chat.listen():
                self.__messages.append(message)
        except Exception as e:
            self.__messages.append(ErrorMessage(e.__str__()))

    def add_chat(self, chat):
        """added chat to chat list, chat should be subclass of \"Chat\" """
        if issubclass(type(chat), Chat):
            self.__chats.append(chat)
        else:
            raise TypeError('object should be subclass of "Chat"')

    def listen(self):
        """listen for a messages from all chats"""
        for chat in self.__chats:
            Thread(target=asyncio.run, args=(self.__save_messages(chat), ), daemon=True).start()

        while 1:
            if self.__messages.__len__() > 0:
                yield self.__messages.pop()
            else:
                sleep(0.1)

    def send_message(self, msg_text):
        """send message to all chats"""
        for chat in self.__chats:
            Thread(target=asyncio.run, args=(chat.send_message(msg_text), ), daemon=True).start()


