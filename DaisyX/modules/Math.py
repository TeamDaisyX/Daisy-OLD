import json
import math
import requests
from telethon import types
from telethon.tl import functions
from DaisyX.decorator import register
from .utils.disable import disableable_dec
from .utils.message import get_arg
#from DaisyX.services.mongo import db
from .utils.message import get_args_str


@register(cmds=['simplify', 'solve'])
@disableable_dec('simplify')
async def _(message):
    args = get_args_str(message)
    response = requests.get(f"https://newton.now.sh/api/v2/simplify/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await message.reply(j)
    
@register(cmds=['factor', 'factorize'])
@disableable_dec('factor')
async def _(message):
    args = get_args_str(message)
    response = requests.get(f"https://newton.now.sh/api/v2/factor/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await message.reply(j)

    
