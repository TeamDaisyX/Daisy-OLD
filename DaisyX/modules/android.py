# This file is part of TeamDaisyX's Daisy-X (Telegram Bot)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import rapidjson as json
from requests import get
from yaml import load, Loader
from bs4 import BeautifulSoup

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from DaisyX.decorator import register
from .utils.android import GetDevice
from .utils.disable import disableable_dec
from .utils.message import get_arg

MIUI_FIRM = "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/data/latest.yml"
REALME_FIRM = "https://raw.githubusercontent.com/RealmeUpdater/realme-updates-tracker/master/data/latest.yml"


@register(cmds='whatis')
@disableable_dec('whatis')
async def whatis(message):
    device = get_arg(message)
    if not device:
        m = "Please write your codename into it, i.e <code>/whatis raphael</code>"
        await message.reply(m)
        return

    data = GetDevice(device).get()
    if data:
        name = data['name']
        device = data['device']
        brand = data['brand']
        model = data['model']
    else:
        m = "coudn't find your device, check device & try!"
        await message.reply(m)
        return

    m = f'<b>{device}</b> is <code>{brand} {name}</code>\n'
    await message.reply(m)


@register(cmds='variants')
@disableable_dec('variants')
async def variants(message):
    device = get_arg(message)
    if not device:
        m = "Please write your codename into it, i.e <code>/specs herolte</code>"
        await message.reply(m)
        return

    data = GetDevice(device).get()
    if data:
        name = data['name']
        device = data['device']
    else:
        m = "coudn't find your device, chack device & try!"
        await message.reply(m)
        return

    data = get(
        'https://raw.githubusercontent.com/androidtrackers/certified-android-devices/master/by_device.json').content
    db = json.loads(data)
    device = db[device]
    m = f'<b>{name}</b> variants:\n\n'

    for i in device:
        name = i['name']
        model = i['model']
        m += '<b>Model</b>: <code>{}</code> \n<b>Name:</b> <code>{}</code>\n\n'.format(
            model, name)

    await message.reply(m)


@register(cmds='miui')
@disableable_dec('miui')
async def miui(message):
    codename = get_arg(message)
    if not codename:
        m = "Please write a codename, example: <code>/miui whyred</code>"
        await message.reply(m)
        return

    yaml_data = load(get(MIUI_FIRM).content, Loader=Loader)
    data = [i for i in yaml_data if codename in i['codename']]

    if len(data) < 1:
        await message.reply("Provide a valid codename!")
        return

    for fw in data:
        av = fw['android']
        branch = fw['branch']
        method = fw['method']
        link = fw['link']
        fname = fw['name']
        version = fw['version']
        size = fw['size']
        date = fw['date']
        md5 = fw['md5']
        codename = fw['codename']

        btn = branch + ' | ' + method + ' | ' + version

        button = InlineKeyboardMarkup().add(InlineKeyboardButton(text=btn, url=link))

    text = f"<b>MIUI - Last build for {codename}:</b>"
    text += f"\n\n<b>Name:</b> <code>{fname}</code>"
    text += f"\n<b>Android:</b> <code>{av}</code>"
    text += f"\n<b>Size:</b> <code>{size}</code>"
    text += f"\n<b>Date:</b> <code>{date}</code>"
    text += f"\n<b>MD5:</b> <code>{md5}</code>"

    await message.reply(text, reply_markup=button)


@register(cmds='realmeui')
@disableable_dec('realmeui')
async def realmeui(message):
    codename = get_arg(message)
    if not codename:
        m = "Please write a codename, example: <code>/realmeui RMX2061</code>"
        await message.reply(m)
        return

    yaml_data = load(get(REALME_FIRM).content, Loader=Loader)
    data = [i for i in yaml_data if codename in i['codename']]

    if len(data) < 1:
        await message.reply("Provide a valid codename!")
        return

    for fw in data:
        reg = fw['region']
        link = fw['download']
        device = fw['device']
        version = fw['version']
        cdn = fw['codename']
        sys = fw['system']
        size = fw['size']
        date = fw['date']
        md5 = fw['md5']

        btn = reg + ' | ' + version

        button = InlineKeyboardMarkup().add(InlineKeyboardButton(text=btn, url=link))

    text = f"<b>RealmeUI - Last build for {codename}:</b>"
    text += f"\n\n<b>Device:</b> <code>{device}</code>"
    text += f"\n<b>System:</b> <code>{sys}</code>"
    text += f"\n<b>Size:</b> <code>{size}</code>"
    text += f"\n<b>Date:</b> <code>{date}</code>"
    text += f"\n<b>MD5:</b> <code>{md5}</code>"

    await message.reply(text, reply_markup=button)


@register(cmds='magisk')
@disableable_dec('magisk')
async def magisk(message):
    url = 'https://raw.githubusercontent.com/topjohnwu/magisk_files/'
    releases = '<b>Latest Magisk Releases:</b>\n'
    variant = ['master/stable', 'master/beta', 'canary/canary']
    for variants in variant:
        fetch = get(url + variants + '.json')
        data = json.loads(fetch.content)
        if variants == "master/stable":
            name = "<b>Stable</b>"
            cc = 0
            branch = "master"
        elif variants == "master/beta":
            name = "<b>Beta</b>"
            cc = 0
            branch = "master"
        elif variants == "canary/canary":
            name = "<b>Canary</b>"
            cc = 1
            branch = "canary"

        if variants == "canary/canary":
            releases += f'{name}: <a href="{url}{branch}/{data["magisk"]["link"]}">ZIP v{data["magisk"]["version"]}</a> | ' \
                        f'<a href="{url}{branch}/{data["app"]["link"]}">APK v{data["app"]["version"]}</a> | '
        else:
            releases += f'{name}: <a href="{url}{branch}/{data["magisk"]["link"]}">ZIP v{data["magisk"]["version"]}</a> | ' \
                        f'<a href="{data["app"]["link"]}">APK v{data["app"]["version"]}</a> | '

        if cc == 1:
            releases += f'<a href="{url}{branch}/{data["uninstaller"]["link"]}">Uninstaller</a> | ' \
                        f'<a href="{url}{branch}/notes.md">Changelog</a>\n'
        else:
            releases += f'<a href="{data["uninstaller"]["link"]}">Uninstaller</a>\n'

    await message.reply(releases, disable_web_page_preview=True)


@register(cmds='phh')
@disableable_dec('phh')
async def phh(message):
    fetch = get(
        "https://api.github.com/repos/phhusson/treble_experimentations/releases/latest"
    )
    usr = json.loads(fetch.content)
    text = "<b>Phh's latest GSI release(s):</b>\n"
    for i in range(len(usr)):
        try:
            name = usr['assets'][i]['name']
            url = usr['assets'][i]['browser_download_url']
            text += f"<a href='{url}'>{name}</a>\n"
        except IndexError:
            continue
    await message.reply(text)


@register(cmds='phhmagisk')
@disableable_dec('phhmagisk')
async def phh_magisk(message):
    fetch = get(
        "https://api.github.com/repos/expressluke/phh-magisk-builder/releases/latest"
    )
    usr = json.loads(fetch.content)
    text = "<b>Phh's latest Magisk release(s):</b>\n"
    for i in range(len(usr)):
        try:
            name = usr['assets'][i]['name']
            url = usr['assets'][i]['browser_download_url']
            tag = usr['tag_name']
            size_bytes = usr['assets'][i]['size']
            size = float("{:.2f}".format((size_bytes/1024)/1024))
            text += f"<b>Tag:</b> <code>{tag}</code>\n"
            text += f"<b>Size</b>: <code>{size} MB</code>\n\n"
            btn = "Click here to download!"
            button = InlineKeyboardMarkup().add(InlineKeyboardButton(text=btn, url=url))
        except IndexError:
            continue
    await message.reply(text, reply_markup=button)
    return


@register(cmds='twrp')
@disableable_dec('twrp')
async def twrp(message):
    device = get_arg(message).lower()

    if not device:
        m = "Type the device codename, example: <code>/twrp j7xelte</code>"
        await message.reply(m)
        return

    url = get(f'https://eu.dl.twrp.me/{device}/')
    if url.status_code == 404:
        m = "TWRP is not available for <code>{device}</code>"
        await message.reply(m)
        return

    else:
        m = f'<b>Latest TWRP for {device}</b>\n'
        page = BeautifulSoup(url.content, 'lxml')
        date = page.find("em").text.strip()
        m += f'📅 <b>Updated:</b> <code>{date}</code>\n'
        trs = page.find('table').find_all('tr')
        row = 2 if trs[0].find('a').text.endswith('tar') else 1

        for i in range(row):
            download = trs[i].find('a')
            dl_link = f"https://dl.twrp.me{download['href']}"
            dl_file = download.text
            size = trs[i].find("span", {"class": "filesize"}).text
        m += f'📥 <b>Size:</b> <code>{size}</code>\n'
        m += f'📦 <b>File:</b> <code>{dl_file.lower()}</code>'
        btn = "Click here to download!"
        button = InlineKeyboardMarkup().add(InlineKeyboardButton(text=btn, url=dl_link))
        await message.reply(m, reply_markup=button)


@register(cmds='samcheck')
@disableable_dec('samcheck')
async def check(message):
    try:
        msg_args = message.text.split()
        temp = msg_args[1]
        csc = msg_args[2]
    except IndexError:
        m = "Please type your device <b>MODEL</b> and <b>CSC</b> into it!\ni.e <code>/samcheck SM-J710MN ZTO</code>!"
        await message.reply(m)
        return

    model = 'sm-' + temp if not temp.upper().startswith('SM-') else temp
    fota = get(
        f'http://fota-cloud-dn.ospserver.net/firmware/{csc.upper()}/{model.upper()}/version.xml')
    test = get(
        f'http://fota-cloud-dn.ospserver.net/firmware/{csc.upper()}/{model.upper()}/version.test.xml')
    if test.status_code != 200:
        m = f"Couldn't find any firmwares for {temp.upper()} - {csc.upper()}, please refine your search or try again later!"
        await message.reply(m)
        return

    page1 = BeautifulSoup(fota.content, 'lxml')
    page2 = BeautifulSoup(test.content, 'lxml')
    os1 = page1.find("latest").get("o")
    os2 = page2.find("latest").get("o")
    if page1.find("latest").text.strip():
        pda1, csc1, phone1 = page1.find("latest").text.strip().split('/')
        m = f'<b>MODEL:</b> <code>{model.upper()}</code>\n<b>CSC:</b> <code>{csc.upper()}</code>\n\n'
        m += '<b>Latest Avaliable Firmware:</b>\n'
        m += f'• PDA: <code>{pda1}</code>\n• CSC: <code>{csc1}</code>\n'
        if phone1:
            m += f'• Phone: <code>{phone1}</code>\n'
        if os1:
            m += f'• Android: <code>{os1}</code>\n'
        m += '\n'
    else:
        m = f'<b>No public release found for {model.upper()} and {csc.upper()}.</b>\n\n'
    m += '<b>Latest Test Firmware:</b>\n'
    if len(page2.find("latest").text.strip().split('/')) == 3:
        pda2, csc2, phone2 = page2.find("latest").text.strip().split('/')
        m += f'• PDA: <code>{pda2}</code>\n• CSC: <code>{csc2}</code>\n'
        if phone2:
            m += f'• Phone: <code>{phone2}</code>\n'
        if os2:
            m += f'• Android: <code>{os2}</code>\n'
    else:
        md5 = page2.find("latest").text.strip()
        m += f'• Hash: <code>{md5}</code>\n• Android: <code>{os2}</code>\n\n'

    await message.reply(m)


__mod_name__ = "Android"

__help__ = """
<b>GSI</b>
- /phh: Get the latest PHH AOSP GSIs.
- /phhmagisk: Get the latest PHH Magisk.

<b>Device firmware:</b>
- /miui (codename): Xiaomi only - gets latest MIUI download links for the given device.
- /realmeui (codename): Realme only - gets latest RealmeUI download links for the given device.
- /samcheck (model) (csc): Samsung only - shows the latest firmware info for the given device, taken from samsung servers.

<b>Misc</b>
- /magisk: Get latest Magisk releases.
- /twrp (codename): Gets latest twrp for the android device using the codename.
- /ofox: Gets the list of officially supported devices by the Orange Fox Recovery Project.
- /ofox (device): Gets the download link and basic OFRP information to the specified device.
- /models (codename): Search for Android device models using codename.
- /whatis (codename): Find out which smartphone is using the codename.
"""
