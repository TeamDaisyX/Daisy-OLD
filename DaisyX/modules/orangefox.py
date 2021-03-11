# This file is part of TeamDaisyX Daisy-X (Telegram Bot)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the`
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import rapidjson as json
from requests import get

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from DaisyX.decorator import register
from .utils.disable import disableable_dec
from .utils.message import get_arg

# orangefox: By @MrYacha, powered by OrangeFox API v2

API_HOST = 'https://api.orangefox.download/v2'


@register(cmds='ofox')
@disableable_dec('ofox')
async def orangefox(message):
    try:
        codename = get_arg(message).lower()
    except Exception:
        codename = ''

    if codename == '':
        reply_text = "<b>OrangeFox Recovery is currently avaible for:</b>"

        devices = _send_request('device/releases/stable')
        for device in devices:
            reply_text += f"\n • {device['fullname']} (<code>{device['codename']}</code>)"

        reply_text += '\n\n' + \
            "You can get latest release by using <code>/ofox (codename)</code>"
        await message.reply(reply_text)
        return

    device = _send_request(f'device/{codename}')
    if not device:
        reply_text = "Device is not found!"
        await message.reply(reply_text)
        return

    release = _send_request(f'device/{codename}/releases/stable/last')
    if not release:
        reply_text = "Release is not found!"
        await message.reply(reply_text)
        return

    reply_text = ("<b>📱 Device:</b> {fullname} (<code>{codename}</code>)\n").format(
        fullname=device['fullname'],
        codename=device['codename']
    )
    reply_text += ("🔺 <b>Version:</b> <code>{}</code>\n").format(
        release['version'])
    reply_text += ("📅 <b>Release date:</b> {}\n").format(release['date'])
    reply_text += ("✅ <b>File MD5:</b> <code>{}</code>\n").format(
        release['md5'])

    if device['maintained'] == 3:
        status = "Not maintained"
    else:
        status = "Maintained"

    reply_text += ("👨‍🔬 <b>Maintainer:</b> {name}, {status}\n").format(
        name=device['maintainer']['name'],
        status=status
    )

    btn = "Click here to download!"
    url = release['url']
    button = InlineKeyboardMarkup().add(InlineKeyboardButton(text=btn, url=url))
    await message.reply(reply_text, reply_markup=button)
    return


def _send_request(endpoint):
    response = get(API_HOST + "/" + endpoint)
    if response.status_code == 404:
        return False

    return json.loads(response.text)
