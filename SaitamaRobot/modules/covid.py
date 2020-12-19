
import datetime
from random import randint
import os
import re
import urllib
from datetime import datetime
import urllib.request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import requests
from typing import List
from SaitamaRobot import dispatcher
from telegram import ParseMode, InputMediaPhoto, Update, TelegramError, ChatAction
from telegram.ext import CommandHandler, run_async, CallbackContext
from SaitamaRobot.modules.disable import DisableAbleCommandHandler

@run_async
def covid(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text.split(' ', 1)
    if len(text) == 1:
        r = requests.get("https://corona.lmao.ninja/v2/all").json()
        reply_text = f"**Global Totals** 🦠\nCases: {r['cases']:,}\nCases Today: {r['todayCases']:,}\nDeaths: {r['deaths']:,}\nDeaths Today: {r['todayDeaths']:,}\nRecovered: {r['recovered']:,}\nActive: {r['active']:,}\nCritical: {r['critical']:,}\nCases/Mil: {r['casesPerOneMillion']}\nDeaths/Mil: {r['deathsPerOneMillion']}"
    else:
        variabla = text[1]
        r = requests.get(
            f"https://corona.lmao.ninja/v2/countries/{variabla}").json()
        reply_text = f"**Cases for {r['country']} 🦠**\nCases: {r['cases']:,}\nCases Today: {r['todayCases']:,}\nDeaths: {r['deaths']:,}\nDeaths Today: {r['todayDeaths']:,}\nRecovered: {r['recovered']:,}\nActive: {r['active']:,}\nCritical: {r['critical']:,}\nCases/Mil: {r['casesPerOneMillion']}\nDeaths/Mil: {r['deathsPerOneMillion']}"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)



COVID_HANDLER = DisableAbleCommandHandler(["covid", "corona"], covid)
dispatcher.add_handler(COVID_HANDLER)

        buffer.save('bob.jpg', 'JPEG')
    for mocked in glob.glob("mocked*"):
        os.remove(mocked)
    reply_text = spongemock.mock(data)

    randint = random.randint(1, 699)
    magick = """convert bob.jpg -font Impact -pointsize 30 -size 512x300 -stroke black -strokewidth 1 -fill white -background none -gravity north caption:"{}" -flatten mocked{}.jpg""".format(reply_text, randint)
    os.system(magick)
    with open('mocked{}.jpg'.format(randint), 'rb') as mockedphoto:
        message.reply_to_message.reply_photo(photo=mockedphoto, reply=message.reply_to_message)
    os.remove('mocked{}.jpg'.format(randint))
    
    


MOCK_HANDLER = DisableAbleCommandHandler("mock", spongemocktext, admin_ok=True)
KIM_HANDLER = DisableAbleCommandHandler("kim", kimtext, admin_ok=True)
HITLER_HANDLER = DisableAbleCommandHandler("hitler", hitlertext, admin_ok=True)


dispatcher.add_handler(MOCK_HANDLER)
dispatcher.add_handler(KIM_HANDLER)
dispatcher.add_handler(HITLER_HANDLER)

__command_list__ = ["mock", "kim", "hitler"]
__handlers__ = [MOCK_HANDLER, KIM_HANDLER,  HITLER_HANDLER]
