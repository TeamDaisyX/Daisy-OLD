
from telethon import TelegramClient
from telethon.sessions import StringSession

ubot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
try:
    ubot.start()
except BaseException:
    print("Userbot Error ! Have you added a STRING_SESSION in deploying??")
    sys.exit(1)
