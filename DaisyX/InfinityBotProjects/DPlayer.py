import os
import ffmpeg
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import LeaveGroupCall
from pytgcalls import GroupCall
import asyncio
import math
import time
from pyrogram import filters
from DaisyX import pbot



VOICE_CHATS = {}
@pbot.on_message(filters.command(["play", "playmusic"]) & ~filters.private)
def config(client, message):

async def test(client, message):
    user = client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status is "administrator" or user.user.id in SUDO_USERS:
        chat_id = message.chat.id
        if not message.reply_to_message and not message.reply_to_message.audio:
            await message.reply("`Reply To Audio To Play It`")
            return
        audio = message.reply_to_message.audio
        audio_original = await message.reply_to_message.download()
        await message.reply_text("`Please Wait, Let Me Download This File!`")
        ffmpeg.input(audio_original).output(
        "stark.raw",
        format='s16le',
        acodec='pcm_s16le',
        ac=2, ar='48k'
        ).overwrite_output().run()
        group_call = GroupCall(client, "stark.raw")
        await group_call.start(message.chat.id)
        await message.edit_text(f"DaisyX now Playing `{audio.title}...` in {message.chat.title}!")
        os.remove(audio_original)
