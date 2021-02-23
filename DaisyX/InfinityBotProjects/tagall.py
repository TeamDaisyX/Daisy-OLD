#    Copyright (C) 2021 by FridayProject & DaisyX
#    This programme is a part of Friday Userbot project
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


from telegram.utils.helpers import mention_html
from telethon import *
from telethon.tl.types import *

from DaisyX import telethn as tbot


@tbot.on(events.NewMessage(pattern="^/tagall (.*) (.*)"))
async def _(event):
    if event.fwd_from:
        return
    chat = await event.get_input_chat()
    mentions = ""
    sh = event.pattern_match.group(1) if event.pattern_match.group(1) else "Hi !"
    async for x in event.client.iter_participants(chat):
        mentions += "[{}](tg://user?id={}) \n".format(mention_html(x.first_name, x.id))
    await event.delete()
    n = 4096
    kk = [mentions[i : i + n] for i in range(0, len(mentions), n)]
    for i in kk:
        j = f"**{sh}** \n{i}"
        await event.client.send_message(event.chat_id, j)
