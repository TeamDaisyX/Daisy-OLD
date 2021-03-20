
from telethon import events

@friday.on(friday_on_cmd(pattern="stat$"))
async def stats(event):
    if event.fwd_from:
        return
    ahyes = await tbot.get_me()
    botusername = ahyes.username
    noob = "stats"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await tbot.inline_query(botusername, noob)
    await tap[0].click(event.chat_id)
    await event.delete()

@tbot.on(events.NewMessage(pattern="/xogame$"))
async def gamez(event):
    if event.fwd_from:
        return
    botusername = "@xobot"
    noob = "play"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await tbot.inline_query(botusername, noob)
    await tap[0].click(event.chat_id)
    await event.delete()


@tbot.on(events.NewMessage(pattern="wspr ?(.*)"))
async def wspr(event):
    if event.fwd_from:
        return
    wwwspr = event.pattern_match.group(1)
    botusername = "@whisperBot"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await tbot.inline_query(botusername, wwwspr)
    await tap[0].click(event.chat_id)
    await event.delete()



@tbot.on(events.NewMessage(pattern="mod ?(.*)"))
async def mod(event):
    if event.fwd_from:
        return
    modr = event.pattern_match.group(1)
    botusername = "@PremiumAppBot"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await tbot.inline_query(botusername, modr)
    await tap[0].click(event.chat_id)
    await event.delete()

__mod_nme__ ="Fun Tools"
__help__="""
Syntax - .xogame
Usage - starts a multiplayer xo game
Syntax -.wspr <text> <username/ID>
Usage -sends a inline whisper message for given user
Syntax - .mod <app name>
Usage - Provides mod APK for given app
"""
