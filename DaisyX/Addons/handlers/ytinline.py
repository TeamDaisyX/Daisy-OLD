from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from DaisyX import pbot as Client


@Client.on_message(filters.command("yt") & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    await message.reply_text(
        "💁🏻‍♂️ Do you want to search for a YouTube video?",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("✅ Yes", switch_inline_query_current_chat=""),
                    InlineKeyboardButton("No ❌", callback_data="close"),
                ]
            ]
        ),
    )
