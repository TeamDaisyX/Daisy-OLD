from typing import Callable, Coroutine

from pyrogram import Client
from pyrogram.types import Message

from DaisyX import TIGERS
from helpers.admins import get_administrators


def admins_only(func: Callable) -> Coroutine:
    async def wrapper(client: Client, message: Message):
        if message.from_user.id in TIGERS:
            return await func(client, message)
        admins = await get_administrators(message.chat)
        for admin in admins:
            if admin.id == message.from_user.id:
                return await func(client, message)

    return wrapper
