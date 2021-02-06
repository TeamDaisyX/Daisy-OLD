import json
import math

import requests
from pymongo import MongoClient
from telethon import types
from telethon.tl import functions

from DaisyX import MONGO_DB_URI
from DaisyX import telethn as tbot
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
    return None


@register(pattern="^/simplify (.*)")
async def _(event):
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
    args = event.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/simplify/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await event.reply(j)


@register(pattern="^/factor (.*)")
async def _(event):
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
    args = event.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/factor/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await event.reply(j)


@register(pattern="^/derive (.*)")
async def _(event):
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
    args = event.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/derive/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await event.reply(j)


@register(pattern="^/integrate (.*)")
async def _(event):
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
    args = event.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/integrate/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await event.reply(j)


@register(pattern="^/zeroes (.*)")
async def _(event):
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
    args = event.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/zeroes/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await event.reply(j)


@register(pattern="^/tangent (.*)")
async def _(event):
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
    args = event.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/tangent/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await event.reply(j)


@register(pattern="^/area (.*)")
async def _(event):
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
    args = event.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/area/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await event.reply(j)


@register(pattern="^/cos (.*)")
async def _(event):
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
    args = int(event.pattern_match.group(1))
    await event.reply(str(math.cos(int(args))))


@register(pattern="^/sin (.*)")
async def _(event):
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
    args = int(event.pattern_match.group(1))

    await event.reply(str(math.sin(int(args))))


@register(pattern="^/tan (.*)")
async def _(event):
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
    args = int(event.pattern_match.group(1))

    await event.reply(str(math.tan(int(args))))


@register(pattern="^/arccos (.*)")
async def _(event):
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
    args = int(event.pattern_match.group(1))

    await event.reply(str(math.acos(int(args))))


@register(pattern="^/arcsin (.*)")
async def _(event):
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
    args = int(event.pattern_match.group(1))

    await event.reply(str(math.asin(int(args))))


@register(pattern="^/arctan (.*)")
async def _(event):
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
    args = int(event.pattern_match.group(1))

    await event.reply(str(math.atan(int(args))))


@register(pattern="^/abs (.*)")
async def _(event):
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
    args = int(event.pattern_match.group(1))

    await event.reply(str(math.fabs(int(args))))


@register(pattern="^/log (.*)")
async def _(event):
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
    args = int(event.pattern_match.group(1))

    await event.reply(str(math.log(int(args))))
