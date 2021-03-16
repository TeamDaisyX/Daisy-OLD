#Ported from Friday
import os
import requests
from telethon import types
from telethon.tl import functions
from telethon import events
from DaisyX.services.events import register
from DaisyX.function.telethonhelpers import convert_to_image
import json
import requests
from DaisyX.services.telethon import tbot
sedpath = "./"
if not os.path.isdir(sedpath):
    os.makedirs(sedpath)

@register(pattern=r"^/yandex(?: |$)([\s\S]*)")
async def hmm(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.reply("Reply to any Image.")
        return
    hmmu = await event.reply("hmm... Reverse Searching The Image On Yandex...🚶")
    sed = await event.get_reply_message()
    img = await convert_to_image(event, borg)
    filePath = img
    searchUrl = 'https://yandex.ru/images/search'
    files = {'upfile': ('blob', open(filePath, 'rb'), 'image/jpeg')}
    params = {'rpt': 'imageview', 'format': 'json', 'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
    response = requests.post(searchUrl, params=params, files=files)
    query_string = json.loads(response.content)['blocks'][0]['params']['url']
    img_search_url= searchUrl + '?' + query_string
    caption = f"""<b>Reverse Search Conpleted!</b>
Reverse Searched Link:- {img_search_url}
Note:- Yandex is a Russian search engine, so better open link in chrome with auto-translate.
Another Note:- Don't Use This Command continually, Yandex Will Block Your Request.
<u><b>Reverse Search Completed By @DaisyXBot.
Say Hi to the Support @DaisySupport_Official.</b></u>
"""
    await tbot.send_message(
        event.chat_id,
        caption,
        parse_mode="HTML",
    )
    await event.delete()
    
