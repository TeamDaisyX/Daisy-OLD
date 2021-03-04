import os

import ffmpeg
from pyrogram import filters
from pytgcalls import GroupCall

from DaisyX import pbot

VOICE_CHATS = {}


@pbot.on_message(filters.command(["play", "playmusic"]) & ~filters.private)
async def test(client, message):
    client.get_chat_member(message.chat.id, message.from_user.id)
    if client.get_chat_member(chat_id, user_id).status in ("administrator", "creator"):
        message.chat.id
        message.chat.id
        if not message.reply_to_message and not message.reply_to_message.audio:
            await message.reply("`Reply To Audio To Play It`")
            return
        audio = message.reply_to_message.audio
        audio_original = await message.reply_to_message.download()
        await message.reply_text("`Please Wait, Let Me Download This File!`")
        ffmpeg.input(audio_original).output(
            "stark.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
        ).overwrite_output().run()
        group_call = GroupCall(client, "stark.raw")
        await group_call.start(message.chat.id)
        await message.edit_text(
            f"DaisyX now Playing `{audio.title}...` in {message.chat.title}!"
        )
        os.remove(audio_original)
