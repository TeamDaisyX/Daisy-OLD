#    Copyright (C) 2020-2021 by @InukaAsith
#    This programme is a part of DaisyX TG bot project
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


import logging
import time

from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameNotOccupied,
    UserNotParticipant,
)
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from DaisyX import DRAGONS as SUDO_USERS
from DaisyX import pbot
from DaisyX.modules.sql import forceSubscribe_sql as sql

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(
    lambda _, __, query: query.data == "onUnMuteRequest"
)


@pbot.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
    user_id = cb.from_user.id
    chat_id = cb.message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        channel = chat_db.channel
        chat_member = client.get_chat_member(chat_id, user_id)
        if chat_member.restricted_by:
            if chat_member.restricted_by.id == (client.get_me()).id:
                try:
                    client.get_chat_member(channel, user_id)
                    client.unban_chat_member(chat_id, user_id)
                    cb.message.delete()
                    # if cb.message.reply_to_message.from_user.id == user_id:
                    # cb.message.delete()
                except UserNotParticipant:
                    client.answer_callback_query(
                        cb.id,
                        text=f"❗ අපේ @{channel} channel එකට Join වෙලා 'UnMute Me' button එක ආපහු ඔබන්න.",
                        show_alert=True,
                    )
            else:
                client.answer_callback_query(
                    cb.id,
                    text="❗ ඔයාව වෙන හේතුවක් නිසා Admin ල mute කරලයි ඉන්නෙ.",
                    show_alert=True,
                )
        else:
            if (
                not client.get_chat_member(chat_id, (client.get_me()).id).status
                == "administrator"
            ):
                client.send_message(
                    chat_id,
                    f"❗ **{cb.from_user.mention} is trying to UnMute himself but i can't unmute him because i am not an admin in this chat add me as admin again.**\n__#Leaving this chat...__",
                )

            else:
                client.answer_callback_query(
                    cb.id,
                    text="❗ අවවාදයයි: ඔයාට කතාකරන්න පුලුවන්කම තියෙද්දි button එක click කරන්න එපා.",
                    show_alert=True,
                )


@pbot.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
    chat_id = message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        user_id = message.from_user.id
        if (
            not client.get_chat_member(chat_id, user_id).status
            in ("administrator", "creator")
            and not user_id in SUDO_USERS
        ):
            channel = chat_db.channel
            try:
                client.get_chat_member(channel, user_id)
            except UserNotParticipant:
                try:
                    sent_message = message.reply_text(
                        "ආයුබෝවන් {} 🙏 \n \n **ඔයා අපේ @{} Channel එකට තාම Join වෙලා නෑ** 😭 \n කරුණාකරල ඒකට Join වෙලා පහල තියන **UNMUTE ME** Button එක touch කරන්න. \n \n **[👉 OUR CHANNEL 👈](https://t.me/{})**".format(
                            message.from_user.mention, channel, channel
                        ),
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "UnMute Me", callback_data="onUnMuteRequest"
                                    )
                                ]
                            ]
                        ),
                    )
                    client.restrict_chat_member(
                        chat_id, user_id, ChatPermissions(can_send_messages=False)
                    )
                except ChatAdminRequired:
                    sent_message.edit(
                        "❗ **මම මේකෙ Admin නෙමෙයි..**\n__මට Ban Permissions එක්ක Admin දීල ආපහු උත්සාහ කරන්න.. \n#Ending FSub...__"
                    )

            except ChatAdminRequired:
                client.send_message(
                    chat_id,
                    text=f"❗ **මම @{channel} එකේ Admin නෙමෙයි.**\n__මට ඒකෙ Admin දීල ආපහු Add කරන්න.\n#Leaving this chat...__",
                )


@pbot.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
def config(client, message):
    user = client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status is "creator" or user.user.id in SUDO_USERS:
        chat_id = message.chat.id
        if len(message.command) > 1:
            input_str = message.command[1]
            input_str = input_str.replace("@", "")
            if input_str.lower() in ("off", "no", "disable"):
                sql.disapprove(chat_id)
                message.reply_text("❌ **Force Subscribe is Disabled Successfully.**")
            elif input_str.lower() in ("clear"):
                sent_message = message.reply_text(
                    "**Unmuting all members who are muted by me...**"
                )
                try:
                    for chat_member in client.get_chat_members(
                        message.chat.id, filter="restricted"
                    ):
                        if chat_member.restricted_by.id == (client.get_me()).id:
                            client.unban_chat_member(chat_id, chat_member.user.id)
                            time.sleep(1)
                    sent_message.edit("✅ **UnMuted all members who are muted by me.**")
                except ChatAdminRequired:
                    sent_message.edit(
                        "❗ **I am not an admin in this chat.**\n__I can't unmute members because i am not an admin in this chat make me admin with ban user permission.__"
                    )
            else:
                try:
                    client.get_chat_member(input_str, "me")
                    sql.add_channel(chat_id, input_str)
                    message.reply_text(
                        f"✅ **Force Subscribe is Enabled**\n__Force Subscribe is enabled, all the group members have to subscribe this [channel](https://t.me/{input_str}) in order to send messages in this group.__",
                        disable_web_page_preview=True,
                    )
                except UserNotParticipant:
                    message.reply_text(
                        f"❗ **Not an Admin in the Channel**\n__I am not an admin in the [channel](https://t.me/{input_str}). Add me as a admin in order to enable ForceSubscribe.__",
                        disable_web_page_preview=True,
                    )
                except (UsernameNotOccupied, PeerIdInvalid):
                    message.reply_text(f"❗ **Invalid Channel Username.**")
                except Exception as err:
                    message.reply_text(f"❗ **ERROR:** ```{err}```")
        else:
            if sql.fs_settings(chat_id):
                message.reply_text(
                    f"✅ **Force Subscribe is enabled in this chat.**\n__For this [Channel](https://t.me/{sql.fs_settings(chat_id).channel})__",
                    disable_web_page_preview=True,
                )
            else:
                message.reply_text("❌ **Force Subscribe is disabled in this chat.**")
    else:
        message.reply_text(
            "❗ **Group Creator Required**\n__You have to be the group creator to do that.__"
        )


__help__ = """
*ForceSubscribe:*

*Channel Manageer Inbuilt*
✪ ඔයාගෙ ගෲප් එකේ මෙම්බර්ස්ල Channel එකක් හෝ කිහිපයක් Subscribe කරනකන් Message දාන එක නවත්තන්න මට පුලූවන්.
✪ සාමාජිකයන් ඔබේ Channel  එකට සම්බන්ධ නොවූයේ නම් මම ඔවුන්ව නිශ්ශබ්ද කර channel එකට සම්බන්ධ වන ලෙස පවසන්න සහ බොත්තමක් එබීමෙන් ඔවුන්ව නිශ්ශබ්ද කරන්න මට පුලුවන්.

*Setup*
1) First of all add me in the group as admin with ban users permission and in the channel as admin.
Note: Only creator of the group can setup me and i will not allow force subscribe again if not done so.
 
*Commmands*
✪ /ForceSubscribe - To get the current settings.
✪ /ForceSubscribe no/off/disable - To turn of ForceSubscribe.
✪ /ForceSubscribe {channel username} - To turn on and setup the channel.
✪ /ForceSubscribe clear - To unmute all members who muted by me.

Note: /FSub is an alias of /ForceSubscribe

💭 Only on Sinhala 🇱🇰 yet
 
"""
__mod_name__ = "📢 Force Subscribe 💭"
