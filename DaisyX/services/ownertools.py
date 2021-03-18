# Copyright (C) 2018 - 2020 MrYacha.
# Copyright (C) 2020 Jeepeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This file is part of Sophie.
# Ported for DaisyX by @InukaAsith


from __future__ import annotations

from typing import TYPE_CHECKING

from DaisyX.utils.logging import log

if TYPE_CHECKING:
    from aiogram.api.types import Message


class OwnerFunctions:

    @classmethod
    async def restartPyrogram(cls, message: Message) -> None:
        from . import pbot

        user = message.from_user.id if message.from_user else 0
        log.info(f"Restarting pyrogram, initiated by {user}")
        if await pbot.restart():
            await message.answer("Restarted pyrogram successfully!")

    @classmethod
    async def resetPyrogram(cls, message: Message) -> None:
        from . import pbot

        user = message.from_user.id if message.from_user else 0
        log.warning(f"Resetting pyrogram, initiated by {user}")
        if await pbot.log_out():
            await pbot.start()
        await message.answer("Successfully resetted pyrogram!")
