from DaisyX import BOT_ID
import nude
import html
import asyncio
from DaisyX.modules.sql import cleaner_sql as sql
from pymongo import MongoClient
from DaisyX import MONGO_DB_URI
from DaisyX.events import register
from telethon import types, events
from telethon.tl import *
from telethon.tl.types import *
from DaisyX import *
import better_profanity
from better_profanity import profanity
from textblob import TextBlob

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve
spammers = db.spammer
cleanservices = db.cleanservice
globalchat = db.globchat

CMD_STARTERS = "/"
profanity.load_censor_words_from_file("./profanity_wordlist.txt")


async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )


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


@register(pattern="^/cleanbluetext ?(.*)")
async def _(event):
    if event.is_group:
        if not await can_change_info(message=event):
            return
    else:
        return
    args = event.pattern_match.group(1)
    if args:
        val = args
        if val in ("off", "no"):
            sql.set_cleanbt(event.chat_id, False)
            reply = "Bluetext cleaning has been disabled for <b>{}</b>".format(
                html.escape(event.chat.title)
            )
            await event.reply(reply, parse_mode="html")

        elif val in ("yes", "on"):
            sql.set_cleanbt(event.chat_id, True)
            reply = "Bluetext cleaning has been enabled for <b>{}</b>".format(
                html.escape(event.chat.title)
            )
            await event.reply(reply, parse_mode="html")

        else:
            reply = "Invalid argument.Accepted values are 'yes', 'on', 'no', 'off'"
            await event.reply(reply, parse_mode="html")
    else:
        clean_status = sql.is_enabled(event.chat_id)
        clean_status = "Enabled" if clean_status else "Disabled"
        reply = "Bluetext cleaning for <b>{}</b> : <b>{}</b>".format(
            event.chat.title, clean_status
        )
        await event.reply(reply, parse_mode="html")


@register(pattern="^/ignorecleanbluetext ?(.*)")
async def _(event):
    if event.is_group:
        if not await can_change_info(message=event):
            return
    else:
        return
    args = event.pattern_match.group(1)
    chat = event.chat

    if args is not None:
        val = args
        added = sql.chat_ignore_command(chat.id, val)
        if added:
            reply = "<b>{}</b> has been added to bluetext cleaner ignore list.".format(
                args
            )
        else:
            reply = "Command is already ignored."
        await event.reply(reply, parse_mode="html")

    else:
        reply = "No command supplied to be ignored."
        await event.reply(reply)


@register(pattern="^/unignorecleanbluetext ?(.*)")
async def _(event):
    if event.is_group:
        if not await can_change_info(message=event):
            return
    else:
        return
    args = event.pattern_match.group(1)
    chat = event.chat

    if args is not None:
        val = args
        added = sql.chat_unignore_command(chat.id, val)
        if added:
            reply = "<b>{}</b> has been added to bluetext cleaner ignore list.".format(
                args
            )
        else:
            reply = "Command isn't ignored currently."
        await event.reply(reply, parse_mode="html")

    else:
        reply = "No command supplied to be unignored."
        await event.reply(reply)


@register(pattern="^/listcleanbluetext$")
async def _(event):

    if event.is_group:
        if not await can_change_info(message=event):
            return
    else:
        return

    chat = event.chat

    global_ignored_list, local_ignore_list = sql.get_all_ignored(chat.id)
    text = ""

    if global_ignored_list:
        text = "The following commands are currently ignored globally from bluetext cleaning :\n"

        for x in global_ignored_list:
            text += f" - <code>{x}</code>\n"

    if local_ignore_list:
        text += "\nThe following commands are currently ignored locally from bluetext cleaning :\n"

        for x in local_ignore_list:
            text += f" - <code>{x}</code>\n"

    if text == "":
        text = "No commands are currently ignored from bluetext cleaning."
        await event.reply(text)
        return

    await event.reply(text, parse_mode="html")
    return


@tbot.on(events.NewMessage(pattern=None))
async def _(event):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            return
        if str(event.sender_id) in str(userss) and str(event.chat_id) in str(iid):
            return
        pass
    else:
        return
    if str(event.sender_id) == str(BOT_ID):
        return
    if event.sender_id == OWNER_ID:
        return

    if sql.is_enabled(event.chat_id):
        fst_word = event.text.strip().split(None, 1)[0]
        command = fst_word[1:].split("@")
        if len(fst_word) > 1 and any(
            fst_word.startswith(start) for start in CMD_STARTERS
        ):

            ignored = sql.is_command_ignored(event.chat_id, command[0])
            if ignored:
                return
            await event.delete()


@register(pattern="^/profanity(?: |$)(.*)")
async def profanity(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if MONGO_DB_URI is None:
        return
    if not await can_change_info(message=event):
        return
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


@register(pattern="^/globalmode(?: |$)(.*)")
async def profanity(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if MONGO_DB_URI is None:
        return
    if not await can_change_info(message=event):
        return
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


@register(pattern="^/cleanservice(?: |$)(.*)")
async def cleanservice(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if MONGO_DB_URI is None:
        return
    if not await can_change_info(message=event):
        return
    input = event.pattern_match.group(1)
    chats = cleanservices.find({})
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
    if input in "on":
        if event.is_group:
            chats = cleanservices.find({})
            for c in chats:
                if event.chat_id == c["id"]:
                    await event.reply(
                        "Clean service message already enabled for this chat."
                    )
                    return
            cleanservices.insert_one({"id": event.chat_id})
            await event.reply("I will clean all service messages from now.")
    if input in "off":
        if event.is_group:
            chats = cleanservices.find({})
            for c in chats:
                if event.chat_id == c["id"]:
                    cleanservices.delete_one({"id": event.chat_id})
                    await event.reply("I will not clean service messages anymore.")
                    return
        await event.reply("Service message cleaning isn't turned on for this chat.")

    if not input == "on" and not input == "off":
        await event.reply("I only understand by on or off")
        return


@tbot.on(events.NewMessage(pattern=None))
async def del_profanity(event):
    if event.is_private:
        return
    if MONGO_DB_URI is None:
        return
    msg = str(event.text)
    sender = await event.get_sender()
    let = sender.username
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            return
        pass
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


@tbot.on(events.NewMessage(pattern=None))
async def del_profanity(event):
    if event.is_private:
        return
    if MONGO_DB_URI is None:
        return
    msg = str(event.text)
    sender = await event.get_sender()
    let = sender.username
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            return
        pass
    chats = globalchat.find({})
    for c in chats:
        if event.text:
            if event.chat_id == c["id"]:
                a = TextBlob(msg)
                b = a.detect_language()
                if not b == "en":
                    await event.delete()
                    st = sender.first_name
                    hh = sender.id
                    final = f"[{st}](tg://user?id={hh}) you should only speak in english here !"
                    dev = await event.respond(final)
                    await asyncio.sleep(10)
                    await dev.delete()


@tbot.on(events.ChatAction())
async def del_cleanservice(event):
    chats = cleanservices.find({})
    for c in chats:
        if event.chat_id == c["id"]:
            try:
                await event.delete()
            except Exception as e:
                print(e)

