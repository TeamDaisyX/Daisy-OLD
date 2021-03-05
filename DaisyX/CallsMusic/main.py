from config import API_HASH, API_ID, BOT_TOKEN
from pyrogram import Client as Bot
from tgcalls import run

bot = Bot(
    ":memory:", API_ID, API_HASH, bot_token=BOT_TOKEN, plugins=dict(root="handlers")
)

bot.start()
run()
