import os

import ffmpeg
from pyrogram import filters
from pytgcalls import GroupCall

from DaisyX import pbot
from helpers.wrappers import admins_only

VOICE_CHATS = {}


@pbot.on_message(filters.command(["play", "playmusic"]) & ~filters.private)
@admins_only
async def test(client, message):
    if not message.reply_to_message and not message.reply_to_message.audio:

        await message.reply("`Reply To Audio To Play It`")
        return
    audio = message.reply_to_message.audio
    audio_original = await message.reply_to_message.download()
    await message.reply_text("`Please Wait, Let Me Download This File!`")
    ffmpeg.input(audio_original).output(
        "daisy.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    group_call = GroupCall(client, "daisy.raw")
    await group_call.start(message.chat.id)
    await message.edit_text(
        f"DaisyX now Playing `{audio.title}...` in {message.chat.title}!"
    )
    os.remove(audio_original)
