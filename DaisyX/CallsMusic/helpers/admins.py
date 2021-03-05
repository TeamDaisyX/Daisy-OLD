from typing import List

from pyrogram.types import Chat, User

from DaisyX.CallsMusic.cache.admins import get, set


async def get_members(chat: Chat) -> List[User]:
    _get = get(chat.id)

    if _get:
        return _get
    else:
        set(chat.id, [member.user for member in await chat.get_administrators(filter="administrators")])
        return await get_administrators(chat)
