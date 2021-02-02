from typing import Optional

from telegram import Message, Update, Bot, User
from telegram import MessageEntity
from telegram.error import BadRequest
from telegram.ext import Filters, MessageHandler, run_async

from saitamaRobot import dispatcher
from saitamaRobot.modules.disable import DisableAbleCommandHandler, DisableAbleMessageHandler

from saitamaRobot.modules.helper_funcs.alternate import send_message
from saitamaRobot.modules.helper_funcs.chat_status import user_admin

@run_async
@user_admin
def send(update, context):
	args = update.effective_message.text.split(None, 1)
	creply = args[1]
	send_message(update.effective_message, creply)
	
	
		



ADD_CCHAT_HANDLER = DisableAbleCommandHandler("snd", send)
dispatcher.add_handler(ADD_CCHAT_HANDLER)
__command_list__ = ["snd"]
__handlers__ = [
    ADD_CCHAT_HANDLER
]
