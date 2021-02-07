import threading

from sqlalchemy import Column, String

from DaisyX.modules.sql import BASE, SESSION


class AllowedChat(BASE):
    __tablename__ = "chat_added"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)  # chat_id is int, make sure it is string


AllowedChat.__table__.create(checkfirst=True)

ALLOWCHATLOCK = threading.RLock()

HSLIST = set()


def __load_added_chats_list():  # load shit to memory to be faster, and reduce disk access
    global HSLIST
    try:
        HSLIST = {x.chat_id for x in SESSION.query(AllowedChat).all()}
    finally:
        SESSION.close()


def addedChat(chat_id):
    with ALLOWCHATLOCK:
        chat = SESSION.query(AllowedChat).get(chat_id)
        if not chat:
            chat = AllowedChat(chat_id)
            SESSION.merge(chat)
        SESSION.commit()
        __load_added_chats_list()


def removedChat(chat_id):
    with ALLOWCHATLOCK:
        chat = SESSION.query(AllowedChat).get(chat_id)
        if chat:
            SESSION.delete(chat)
        SESSION.commit()
        __load_added_chats_list()


def isAdded(chat_id):
    return chat_id in HSLIST


__load_added_chats_list()
