# Written by Inukaasith for the Daisy project
# This file is part of DaisyXBot (Telegram Bot)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.



import json
import math
import requests
from telethon import types
from telethon.tl import functions
from DaisyX.decorator import register
from .utils.disable import disableable_dec
from .utils.message import get_arg
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

@register(cmds='derive')
@disableable_dec('derive')    
    args = get_args_str(message)
    response = requests.get(f"https://newton.now.sh/api/v2/derive/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await message.reply(j)    

@register(cmds='integrate')
@disableable_dec('integrate')    
    args = get_args_str(message)
    response = requests.get(f"https://newton.now.sh/api/v2/integrate/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await message.reply(j)
    
@register(cmds='zeroes')
@disableable_dec('zeroes')    
    args = get_args_str(message)
    response = requests.get(f"https://newton.now.sh/api/v2/zeroes/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await message.reply(j)   
    
@register(cmds='tangent')
@disableable_dec('tangent')    
    args = get_args_str(message)
    response = requests.get(f"https://newton.now.sh/api/v2/tangent/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await message.reply(j)   
    
@register(cmds='area')
@disableable_dec('area')    
    args = get_args_str(message)
    response = requests.get(f"https://newton.now.sh/api/v2/area/{args}")
    c = response.text
    obj = json.loads(c)
    j = obj["result"]
    await message.reply(j)      
    
@register(cmds='cos')
@disableable_dec('cos')    
    args = get_args_str(message) 
    await message.reply(str(math.cos(int(args))))
    
@register(cmds='sin')
@disableable_dec('sin')    
    args = get_args_str(message) 
    await message.reply(str(math.sin(int(args))))    
    
@register(cmds='tan')
@disableable_dec('tan')    
    args = get_args_str(message) 
    await message.reply(str(math.tan(int(args))))        
    
@register(cmds='arccos')
@disableable_dec('arccos')    
    args = get_args_str(message) 
    await message.reply(str(math.acos(int(args))))       
      
@register(cmds='arcsin')
@disableable_dec('arcsin')    
    args = get_args_str(message) 
    await message.reply(str(math.asin(int(args))))        
    
@register(cmds='arctan')
@disableable_dec('arctan')    
    args = get_args_str(message) 
    await message.reply(str(math.atan(int(args))))    
    
@register(cmds='abs')
@disableable_dec('abs')    
    args = get_args_str(message) 
    await message.reply(str(math.fabs(int(args))))        
    
@register(cmds='log')
@disableable_dec('log')    
    args = get_args_str(message) 
    await message.reply(str(math.log(int(args))))        
