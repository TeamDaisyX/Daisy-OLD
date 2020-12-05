#Made By @Madepranav On Telegram & Github Id Superboyfan
import html
import random
import SaitamaRobot.modules.animequotesstring as animequotesstring
from SaitamaRobot import dispatcher
from telegram import ParseMode, Update
from SaitamaRobot.modules.disable import DisableAbleCommandHandler
from telegram.ext import CallbackContext, run_async


@run_async
def animequotes(update: Update, context: CallbackContext):
    update.effective_message.reply_text(random.choice(animequotesstring.ANIMEQUOTES))
   

#FtSasaki Fixed The Anime Quotes Module (ㄒoㄒ)

__mod_name__ = "Anime Quotes"

__help__ = """
 • `animequotes` *:* Random Anime Motivational Quotes
 
"""

ANIMEQUOTES_HANDLER = DisableAbleCommandHandler("animequotes", animequotes)

dispatcher.add_handler(ANIMEQUOTES_HANDLER)


