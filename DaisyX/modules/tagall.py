from DaisyX.services.telethon import tbot as client
from telethon import events


@client.on(events.NewMessage(pattern="/tagall(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "@tagall"
    chat = await event.get_input_chat()
    async for x in client.iter_participants(chat, 100):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await event.reply(mentions)
    await event.delete()
