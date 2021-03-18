#    Copyright (C) @InukaAsith 2020-2021
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


from __future__ import annotations

from typing import TYPE_CHECKING

from DaisyX.utils.logger import log
from DaisyX.services.pyrogram import pbot
if TYPE_CHECKING:
    from aiogram.api.types import Message

from DaisyX.config import get_int_key
OWNER =get_int_key("OWNER_ID", required=True)    
    
@pbot.on_message(filters.command(["pyrorestart"]))    
async def restartPyrogram(cls, message: Message) -> None:                   
    #user = message.from_user.id if message.from_user else 0
    user = client.get_chat_member(message.chat.id, message.from_user.id)
    if user.user.id == OWNER:
      await message.answer(f"Restarting pyrogram, initiated by {user}")
      log.info(f"Restarting pyrogram, initiated by {user}")
      if await pbot.restart():
           await message.answer("Restarted pyrogram successfully!")
            

@pbot.on_message(filters.command(["pyroreset"]))                
async def resetPyrogram(cls, message: Message) -> None:
    #user = message.from_user.id if message.from_user else 0
    user = client.get_chat_member(message.chat.id, message.from_user.id)
    if user.user.id == OWNER:
      await message.answer(f"Resetting pyrogram, initiated by {user}")
      log.warning(f"Resetting pyrogram, initiated by {user}")
      if await pbot.log_out():
          await pbot.start()
      await message.answer("Successfully resetted pyrogram!")

    
