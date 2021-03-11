from DaisyX.decorator import register
from .utils.disable import disableable_dec
from .utils.message import get_arg
from DaisyX.services.mongo import db
import json
import math

import requests
from telethon import types
from telethon.tl import functions

@register(cmds=['simplify', 'solve'])
@disableable_dec('simplify')
async def _(event):
    args = event.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/simplify/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await event.reply(j)
    
@register(cmds=['factor', 'factorize'])
@disableable_dec('factor')
    args = event.pattern_match.group(1)
    response = requests.get(f"https://newton.now.sh/api/v2/factor/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await event.reply(j)

    
