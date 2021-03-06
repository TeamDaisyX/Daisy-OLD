from pyrogram import Client

from cache.pytgcalls.pytgcalls import PyTgCalls
from DaisyX import API_HASH, API_ID, SESSION_NAME
from pytgcalls.pytgcalls import PyTgCalls

client = Client(SESSION_NAME, API_ID, API_HASH)
pytgcalls = PyTgCalls(client, 1512, False)


@pytgcalls.on_stream_end()
def on_stream_end(chat_id: int) -> None:
    sira.task_done(chat_id)

    if sira.is_empty(chat_id):
        pytgcalls.leave_group_call(chat_id)
    else:
        pytgcalls.change_stream(chat_id, sira.get(chat_id)["file_path"])


run = pytgcalls.run
