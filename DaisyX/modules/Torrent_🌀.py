from DaisyX import telethn as tbot
import os
import subprocess
import urllib.request
from typing import List
from typing import Optional
import telegraph
from pymongo import MongoClient
from telegraph import Telegraph
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *

from DaisyX import *
from DaisyX.events import register

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):
        ui = await tbot.get_peer_id(user)
        ps = (
            await tbot(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return False


telegraph = Telegraph()
telegraph.create_account(short_name="Julia")


@register(pattern="^/torrent (.*)")
async def tor_search(event):
    if event.fwd_from:
        return
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    str = event.pattern_match.group(1)
    let = f'"{str}"'
    jit = subprocess.check_output(["we-get", "-s", let, "-t", "all", "-J"])
    proc = jit.decode()
    sit = proc.replace("{", "")
    pit = sit.replace("}", "")
    op = pit.replace(",", "")
    seta = f"Magnets for {str} are below:"
    response = telegraph.create_page(seta, html_content=op)
    await event.reply(
        "Magnet Links for {}:\n\nhttps://telegra.ph/{}".format(str, response["path"]),
        link_preview=False,
    )

@register(pattern="^/helptorrent$")
async def howdoi(event):
    if event.fwd_from:
        return
    if not event.is_private:
        return
    c = event.message
    os.system("youtube-dl https://vimeo.com/486829727")
    await tbot.send_file(event.chat_id, "Torrent-486829727.mp4", reply_to=c)
    os.remove("Torrent-486829727.mp4")



__help__ = """
 - /torrent <text>: Search for torrent links
If you are still messed up send `/helptorrent` in pm for the tutorial !
"""

__mod_name__ = "Torrent 🌀"
