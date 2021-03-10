# Copyright (C) 2018 - 2020 MrYacha. All rights reserved. Source code available under the AGPL.
# Copyright (C) 2019 Aiogram

#
# This file is part of AllMightBot.
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

import io

from aiogram.types.input_file import InputFile

from DaisyX import bot
from DaisyX.decorator import register
from .utils.disable import disableable_dec
from .utils.language import get_strings_dec


@register(cmds='getsticker')
@disableable_dec('getsticker')
@get_strings_dec('stickers')
async def get_sticker(message, strings):
    if 'reply_to_message' not in message or 'sticker' not in message.reply_to_message:
        await message.reply(strings['rpl_to_sticker'])
        return

    sticker = message.reply_to_message.sticker
    file_id = sticker.file_id
    text = strings['ur_sticker'].format(emoji=sticker.emoji, id=file_id)

    sticker_file = await bot.download_file_by_id(file_id, io.BytesIO())

    await message.reply_document(
        InputFile(sticker_file, filename=f'{sticker.set_name}_{sticker.file_id[:5]}.png'),
        text
    )


__mod_name__ = "Stickers"

__help__ = """
Stickers are the best way to show emotion.

<b>Available commands:</b>
- /getsticker: Give the sticker image and ID.
"""
