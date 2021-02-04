import os
import subprocess

import requests
from gtts import gTTS, gTTSError
from pymongo import MongoClient
from requests import get
from telethon import *
from telethon.tl import functions, types
from telethon.tl.types import *

from DaisyX import *
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


@register(pattern=r"^/julia(?: |$)([\s\S]*)")
async def _(event):
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
    if not event.reply_to_msg_id:
        i = event.pattern_match.group(1)
        appid = WOLFRAM_ID
        server = f"https://api.wolframalpha.com/v1/spoken?appid={appid}&i={i}"
        res = get(server)
        if res == "Wolfram Alpha did not understand your input":
            await event.reply("Sorry I can't understand")
            return
        await event.reply(f"**{i}**\n\n" + res.text, parse_mode="markdown")

    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        required_file_name = await tbot.download_media(
            previous_message, TEMP_DOWNLOAD_DIRECTORY
        )
        if IBM_WATSON_CRED_URL is None or IBM_WATSON_CRED_PASSWORD is None:
            await event.reply(
                "You need to set the required ENV variables for this module. \nModule stopping"
            )
        else:
            headers = {
                "Content-Type": previous_message.media.document.mime_type,
            }
            data = open(required_file_name, "rb").read()
            response = requests.post(
                IBM_WATSON_CRED_URL + "/v1/recognize",
                headers=headers,
                data=data,
                auth=("apikey", IBM_WATSON_CRED_PASSWORD),
            )
            r = response.json()
            if "results" in r:
                # process the json to appropriate string format
                results = r["results"]
                transcript_response = ""
                for alternative in results:
                    alternatives = alternative["alternatives"][0]
                    transcript_response += " " + str(alternatives["transcript"])
                if transcript_response != "":
                    string_to_show = "{}".format(transcript_response)
                    appid = WOLFRAM_ID
                    server = f"https://api.wolframalpha.com/v1/spoken?appid={appid}&i={string_to_show}"
                    res = get(server)
                    answer = res.text
                    try:
                        tts = gTTS(answer, tld="com", lang="en")
                        tts.save("results.mp3")
                    except AssertionError:
                        return
                    except ValueError:
                        return
                    except RuntimeError:
                        return
                    except gTTSError:
                        return
                    with open("results.mp3", "r"):
                        await tbot.send_file(
                            event.chat_id,
                            "results.mp3",
                            voice_note=True,
                            reply_to=event.id,
                        )
                    os.remove("results.mp3")
                    os.remove(required_file_name)
                elif (
                    transcript_response == "Wolfram Alpha did not understand your input"
                ):
                    try:
                        answer = "Sorry I can't understand"
                        tts = gTTS(answer, tld="com", lang="en")
                        tts.save("results.mp3")
                    except AssertionError:
                        return
                    except ValueError:
                        return
                    except RuntimeError:
                        return
                    except gTTSError:
                        return
                    with open("results.mp3", "r"):
                        await tbot.send_file(
                            event.chat_id,
                            "results.mp3",
                            voice_note=True,
                            reply_to=event.id,
                        )
                    os.remove("results.mp3")
                    os.remove(required_file_name)
            else:
                await event.reply("API Failure !")
                os.remove(required_file_name)


@register(pattern="^/howdoi (.*)")
async def howdoi(event):
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
    jit = subprocess.check_output(["howdoi", f"{str}"])
    pit = jit.decode()
    await event.reply(pit)


__help__ = """
**For text assistant**
 - /julia <question>: Ask julia any question and it will give accurate reply. For eg: `/julia where is Taj Mahal`, `/julia what is the age of Virat Kohli` etc..
**For voice assistant**
 - /julia: Reply to a voice query and get the results in voice output (ENGLISH ONLY)
**Terminal Assistant**
 - /howdoi <question>: Get all coding related answers from Julia. Syntax: `/howdoi print hello world in python`
**NOTE**
The question should be a meaningful one otherwise you will get no response !
"""

__mod_name__ = "Assistant 🤗"
