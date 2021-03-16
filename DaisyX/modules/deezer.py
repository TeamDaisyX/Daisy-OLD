import asyncio
import math
import time
from pyrogram import filters
import wget
import requests
import shutil
import os
import glob
import wget
from youtubesearchpython import SearchVideos
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

from DaisyX.functions.pluginhelpers import get_readable_time, delete_or_pass, progress,get_text
from DaisyX.services.pyrogram import pbot as tbot




@tbot.on(events.NewMessage(pattern="^/vsong (.*)"))
async def ytmusic(client, message):
    urlissed = get_text(message)
    if not urlissed:
        await pablo.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return
    pablo = await edit_or_reply(message, f"`Getting {urlissed} From Youtube Servers. Please Wait.`")
    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    thums = mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await event.edit(event, f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    capy = f"**Video Name ➠** `{thum}` \n**Requested For :** `{urlissed}` \n**Channel :** `{thums}` \n**Link :** `{mo}`"
    await client.send_video(message.chat.id, video = open(file_stark, "rb"), duration = int(ytdl_data["duration"]), file_name = str(ytdl_data["title"]), thumb = sedlyf, caption = capy, supports_streaming = True , progress=progress, progress_args=(pablo, c_time, f'`Uploading {urlissed} Song From YouTube Music!`', file_stark))
    await pablo.delete()
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)






@tbot.on(events.NewMessage(pattern="^/song (.*)"))
async def ytmusic(client, message):
    urlissed = get_text(message)
    if not urlissed:
        await pablo.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return
    pablo = await message.reply(message, f"`Getting {urlissed} From Youtube Servers. Please Wait.`")
    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    dur = mio[0]["duration"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    thums = mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "720",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(mo, download=True)
    except Exception as e:
        await pablo.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    capy = f"**Song Name :** `{thum}` \n**Requested For :** `{urlissed}` \n**Channel :** `{thums}` \n**Link :** `{mo}`"
    file_stark = f"{ytdl_data['id']}.mp3"
    await client.send_audio(message.chat.id, audio = open(file_stark, "rb"), duration = int(ytdl_data["duration"]), title = str(ytdl_data["title"]), performer=str(ytdl_data["uploader"]), thumb = sedlyf, caption = capy, progress=progress, progress_args=(pablo, c_time, f'`Uploading {urlissed} Song From YouTube Music!`', file_stark))
    await pablo.delete()
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)
    


@tbot.on(events.NewMessage(pattern="^/deezer (.*)"))
async def deezer(client, message):
    pablo = await reply(message, "`Searching For Song.....`")
    sgname = get_text(message)
    if not sgname:
        await pablo.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return
    link = f"https://api.deezer.com/search?q={sgname}&limit=1"
    dato = requests.get(url=link).json()
    match = dato.get("data")
    urlhp = (match[0])
    urlp = urlhp.get("link")
    thums = urlhp["album"]["cover_big"]
    thum_f = wget.download(thums)
    polu = urlhp.get("artist")
    replo = urlp[29:]
    urlp = f"https://starkapi.herokuapp.com/deezer/{replo}"
    datto = requests.get(url=urlp).json()
    mus = datto.get("url")
    sname = f"{urlhp.get('title')}.mp3"
    doc = requests.get(mus)
    await client.send_chat_action(message.chat.id, "upload_audio")
    await pablo.edit("`Downloading Song From Deezer!`")
    with open(sname, 'wb') as f:
      f.write(doc.content)
    c_time = time.time()
    await pablo.edit(f"`Downloaded {sname}! Now Uploading Song...`")
    await client.send_audio(message.chat.id, audio = open(sname, "rb"), duration = int(urlhp.get('duration')), title = str(urlhp.get("title")), performer=str(polu.get("name")), thumb = thum_f, progress=progress, progress_args=(pablo, c_time, f'`Uploading {sname} Song From Deezer!`', sname))
    await client.send_chat_action(message.chat.id, "cancel")
    await pablo.delete()

_mod_name_ = "Deezer"

_help_ = """
/deezer : download from deezer
"""
