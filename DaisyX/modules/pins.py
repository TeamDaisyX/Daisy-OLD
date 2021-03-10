# Copyright (C) 2018 - 2020 MrYacha. All rights reserved. Source code available under the AGPL.
# Copyright (C) 2019 Aiogram

#
# This file is part of ProjectDaisyX.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from aiogram.utils.exceptions import BadRequest

from DaisyX import bot
from DaisyX.decorator import register
from .utils.connections import chat_connection
from .utils.language import get_strings_dec
from .utils.message import get_arg


@register(cmds="unpin", user_can_pin_messages=True, bot_can_pin_messages=True)
@chat_connection(admin=True)
@get_strings_dec('pins')
async def unpin_message(message, chat, strings):
    # support unpinning all
    if get_arg(message) in {'all'}:
        return await bot.unpin_all_chat_messages(chat['chat_id'])
    try:
        await bot.unpin_chat_message(chat['chat_id'])
    except BadRequest:
        await message.reply(strings['chat_not_modified_unpin'])
        return


@register(cmds="pin", user_can_pin_messages=True, bot_can_pin_messages=True)
@get_strings_dec('pins')
async def pin_message(message, strings):
    if 'reply_to_message' not in message:
        await message.reply(strings['no_reply_msg'])
        return
    msg = message.reply_to_message.message_id
    arg = get_arg(message).lower()

    dnd = True
    loud = ['loud', 'notify']
    if arg in loud:
        dnd = False

    try:
        await bot.pin_chat_message(message.chat.id, msg, disable_notification=dnd)
    except BadRequest:
        await message.reply(strings['chat_not_modified_pin'])

__mod_name__ = "Pins"

__help__ = """
• /pin: silently pins the message replied to - add 'loud' or 'notify' to give notifs to users
• /unpin: unpins the currently pinned message
"""
