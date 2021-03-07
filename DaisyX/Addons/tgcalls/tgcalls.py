import os

from pyrogram import Client
from pytgcalls.pytgcalls import PyTgCalls

from DaisyX import API_HASH, API_ID, SESSION_NAME

try:
    from pytgcalls.pytgcalls import PyTgCalls
except:
    os.system("curl -sL https://deb.nodesource.com/setup_15.x | bash -")
    os.system("apt-get install -y nodejs")
    os.system("npm i -g npm")
    os.system("git clone https://github.com/pytgcalls/pytgcalls")
    os.system("cd pytgcalls")
    os.system("npm install")
    os.system("npm run prepare")
    os.system("cd pytgcalls/js")
    os.system("npm install")
    os.system("cd ../../")
    os.system("pip3 install -r requirements.txt")
    os.system("cd ../")
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
