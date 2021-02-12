import time

from pymongo import MongoClient
from telethon.tl import *
from telethon.tl.types import *
from tempmail import TempMail

from DaisyX import *
from DaisyX.events import register

from DaisyX import *
from DaisyX.events import register
from tempmail import TempMail

client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
tmail = db.tempmail

tm = TempMail()
api_host = "privatix-temp-mail-v1.p.rapidapi.com"
api_key = TEMP_MAIL_KEY
tm.set_header(api_host, api_key)


@register(pattern="^/registeremail$")
async def _(event):
    if not event.is_private:
        await event.reply("You can only use this service in PM!")
        return
    gmail = tmail.find({})
    for c in gmail:
        if event.sender_id == c["user"]:
            await event.reply(
                "You have already registered your account for this service."
            )
            return
    ttime = time.time()
    email = tm.get_email_address()
    hash = tm.get_hash(email)
    tmail.insert_one({"user": event.sender_id, "time": ttime, "email": hash})
    await event.reply(
        f"You have successfully registered your account !\nYour temporary email is: {email}"
    )


__mod_name__ = "Temp Mail 📧"

__help__ = """
 - /registermail: Registers your account for the tempmail service (one time only)
 - /sendmail <email>: Send the replied message to the email provided (must be a valid one)
 - /checkinbox: Checks the inbox associated with the account for new emails
"""
