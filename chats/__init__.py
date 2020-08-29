import asyncio
from threading import Thread
from time import sleep


class ChatListener():
    def __init__(self):
        self.__chats = []
        self.__twitch_chat = None
        self.__messages = []

    async def __save_message(self, chat):
        async for message in chat.listen():
            self.__messages.append(message)

    def add_chat(self, chat):
        """chat class must have listen(self) method"""
        self.__chats.append(chat)

    def listen(self):
        for chat in self.__chats:
            Thread(target=asyncio.run, args=(self.__save_message(chat), ), daemon=True).start()

        while 1:
            if self.__messages.__len__() > 0:
                yield self.__messages.pop()
            else:
                sleep(0.1)