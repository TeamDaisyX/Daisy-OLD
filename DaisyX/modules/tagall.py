from DaisyX.services.telethon import tbot as client
from telethon import events

@client.on(events.NewMessage(pattern="tagall(?: |$)(.*)"))
async def _(event):
    if event.fwd_from:
        return
    chat = await event.get_input_chat()
    mentions = ""
    sh = event.pattern_match.group(1) if event.pattern_match.group(1) else "Hi !"
    async for x in event.client.iter_participants(chat):
        mentions += f"[{x.first_name}](tg://user?id={x.id}) \n"
    await event.delete()
    n = 4096
    kk = [mentions[i:i+n] for i in range(0, len(mentions), n)]
    for i in kk:
        j = f"**{sh}** \n{i}"
        await event.client.send_message(event.chat_id, j)
