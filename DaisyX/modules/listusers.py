from DaisyX.services.telethon import tbot
from telethon import events
from DaisyX.services.mongo import mongodb as db

approved_users = db.approve


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
    return False

@tbot.on(events.NewMessage(pattern="/listusers(?: |$)(.*)"))
async def _(event):
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    chat = await event.get_input_chat()
    mentions = ""
    sh = event.pattern_match.group(1) if event.pattern_match.group(1) else "Hi !"
    async for x in event.client.iter_participants(chat):
        mentions += f"[{x.first_name}](tg://user?id={x.id}) \n"
    await event.delete()
    n = 4096
    kk = [mentions[i : i + n] for i in range(0, len(mentions), n)]
    for i in kk:
        j = f"**{sh}** \n{i}"
        await event.client.send_message(event.chat_id, j)
