from pyrogram import filters
from pyrogram.types import CallbackQuery

from DaisyX import pbot as Client


@Client.on_callback_query(filters.regex("close"))
async def close(client: Client, query: CallbackQuery):
    await query.message.delete()
