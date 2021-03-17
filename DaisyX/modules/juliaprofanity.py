# This Module is ported from https://github.com/MissJuliaRobot/MissJuliaRobot
# This hardwork was completely done by MissJuliaRobot
# Full Credits goes to MissJuliaRobot

import asyncio

import better_profanity
import nude
from better_profanity import profanity
from telethon import events, types
from telethon.tl import *
from telethon.tl.types import *
from textblob import TextBlob

from DaisyX import *
from DaisyX.services.mongo import mongodb as db
from DaisyX.services.telethon import tbot
from DaisyX.services.events import register

approved_users = db.approve
spammers = db.spammer
globalchat = db.globchat

CMD_STARTERS = "/"
profanity.load_censor_words_from_file("./profanity_wordlist.txt")



@register(pattern="^/profanity(?: |$)(.*)")
async def profanity(event):
    if event.fwd_from:
        return
    if not event.is_group:
        await event.reply("You Can Only profanity in Groups.")
        return
    input_str = event.pattern_match.group(1)
    if not await is_admin(event, BOT_ID): 
        await event.reply("`I Should Be Admin To Do This!`")
        return
    if await is_admin(event, event.message.sender_id): 
        input = event.pattern_match.group(1)
        chats = spammers.find({})
        if not input:
            for c in chats:
                if event.chat_id == c["id"]:
                    await event.reply(
                        "Please provide some input yes or no.\n\nCurrent setting is : **on**"
                    )
                    return
            await event.reply(
                "Please provide some input yes or no.\n\nCurrent setting is : **off**"
            )
            return
        if input == "on":
            if event.is_group:
                chats = spammers.find({})
                for c in chats:
                    if event.chat_id == c["id"]:
                        await event.reply(
                            "Profanity filter is already activated for this chat."
                        )
                        return
                spammers.insert_one({"id": event.chat_id})
                await event.reply("Profanity filter turned on for this chat.")
        if input == "off":
            if event.is_group:
                chats = spammers.find({})
                for c in chats:
                    if event.chat_id == c["id"]:
                        spammers.delete_one({"id": event.chat_id})
                        await event.reply("Profanity filter turned off for this chat.")
                        return
            await event.reply("Profanity filter isn't turned on for this chat.")
        if not input == "on" and not input == "off":
            await event.reply("I only understand by on or off")
            return
    else:
        await event.reply("`You Should Be Admin To Do This!`")
        return

@register(pattern="^/globalmode(?: |$)(.*)")
async def profanity(event):
    if event.fwd_from:
        return
    if not event.is_group:
        await event.reply("You Can Only enable global mode Watch in Groups.")
        return
    input_str = event.pattern_match.group(1)
    if not await is_admin(event, BOT_ID): 
        await event.reply("`I Should Be Admin To Do This!`")
        return
    if await is_admin(event, event.message.sender_id): 

        input = event.pattern_match.group(1)
        chats = globalchat.find({})
        if not input:
            for c in chats:
                if event.chat_id == c["id"]:
                    await event.reply(
                        "Please provide some input yes or no.\n\nCurrent setting is : **on**"
                    )
                    return
            await event.reply(
                "Please provide some input yes or no.\n\nCurrent setting is : **off**"
            )
            return
        if input == "on":
            if event.is_group:
                chats = globalchat.find({})
                for c in chats:
                    if event.chat_id == c["id"]:
                        await event.reply("Global mode is already activated for this chat.")
                        return
                globalchat.insert_one({"id": event.chat_id})
                await event.reply("Global mode turned on for this chat.")
        if input == "off":
            if event.is_group:
                chats = globalchat.find({})
                for c in chats:
                    if event.chat_id == c["id"]:
                        globalchat.delete_one({"id": event.chat_id})
                        await event.reply("Global mode turned off for this chat.")
                        return
            await event.reply("Global mode isn't turned on for this chat.")
        if not input == "on" and not input == "off":
            await event.reply("I only understand by on or off")
            return
    else:
        await event.reply("`You Should Be Admin To Do This!`")
        return

@tbot.on(events.NewMessage(pattern=None))
async def del_profanity(event):
    msg = str(event.text)
    sender = await event.get_sender()
    let = sender.username
    if not event.is_group:
        return
    input_str = event.pattern_match.group(1)
    if not await is_admin(event, BOT_ID): 
        await event.reply("`I Should Be Admin To Do This!`")
        return
    
    if await is_admin(event, event.message.sender_id): 
        chats = spammers.find({})
        for c in chats:
            if event.text:
                if event.chat_id == c["id"]:
                    if better_profanity.profanity.contains_profanity(msg):
                        await event.delete()
                        if sender.username is None:
                            st = sender.first_name
                            hh = sender.id
                            final = f"[{st}](tg://user?id={hh}) **{msg}** is detected as a slang word and your message has been deleted"
                        else:
                            final = f"@{let} **{msg}** is detected as a slang word and your message has been deleted"
                        dev = await event.respond(final)
                        await asyncio.sleep(10)
                        await dev.delete()
            if event.photo:
                if event.chat_id == c["id"]:
                    await event.client.download_media(event.photo, "nudes.jpg")
                    if nude.is_nude("./nudes.jpg"):
                        await event.delete()
                        st = sender.first_name
                        hh = sender.id
                        final = f"[{st}](tg://user?id={hh}) you should only speak in english here !"
                        dev = await event.respond(final)
                        await asyncio.sleep(10)
                        await dev.delete()
                        os.remove("nudes.jpg")
        else:
            await event.reply("`You Should Be Admin To Do This!`")
            return
@tbot.on(events.NewMessage(pattern=None))
async def del_profanity(event):
    if event.is_private:
        return
    msg = str(event.message)
    sender = await event.get_sender()
    sender.username
    if await is_admin(event, event.message.sender_id):
        return
    chats = globalchat.find({})
    for c in chats:
        if event.text:
            if event.chat_id == c["id"]:
                u = msg.split()
                rm = " ".join(filter(lambda x: x[0] != "@", u))
                a = TextBlob(rm)
                b = a.detect_language()
                if not b == "en":
                    await event.delete()
                    st = sender.first_name
                    hh = sender.id
                    final = f"[{st}](tg://user?id={hh}) you should only speak in english here !"
                    dev = await event.respond(final)
                    await asyncio.sleep(10)
                    await dev.delete()
