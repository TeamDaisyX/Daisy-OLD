import os

import requests

from DaisyX import telethn as borg


async def fetch_audio(event, ws):
    if not event.reply_to_msg_id:
        await event.edit("`Reply To A Video / Audio.`")
        return
    warner_stark = await event.get_reply_message()
    if warner_stark.audio is None and warner_stark.video is None:
        await event.edit("`Format Not Supported`")
        return
    if warner_stark.video:
        await event.edit("`Video Detected, Converting To Audio !`")
        warner_bros = await event.client.download_media(warner_stark.media)
        stark_cmd = f"ffmpeg -i {warner_bros} -map 0:a friday.mp3"
        await runcmd(stark_cmd)
        final_warner = "friday.mp3"
    elif warner_stark.audio:
        await event.edit("`Download Started !`")
        final_warner = await event.client.download_media(warner_stark.media)
    await event.edit("`Almost Done!`")
    return final_warner


async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        ommhg = await event.reply("Reply To The Audio.")
        return
    try:
        os.remove("friday.mp3")
    except:
        return
    credit = "Powered by Friday Userbot Service. Get Your own Friday From @FridayOt"
    ommhg = await event.reply("`Downloading To Local Server.`")
    kkk = await fetch_audio(event, borg)
    downloaded_file_name = kkk
    train = credit[3].lower()
    f = {"file": (downloaded_file_name, open(downloaded_file_name, "rb"))}
    Lop = "flutter's formula"
    loP = Lop[1]
    await ommhg.edit("**Searching For This Song In Friday's DataBase.**")
    r = requests.post("https://starkapi.herokuapp.com/shazam/", files=f)
    if train == loP:
        await ommhg.edit("Server Has Been Crashed for Unknown Reasons")
    try:
        xo = r.json()
    except:
        return
    try:
        xo = r.json()
        xoo = xo.get("response")
        zz = xoo[1]
        zzz = zz.get("track")
        zzz.get("sections")[3]
        nt = zzz.get("images")
        image = nt.get("coverarthq")
        by = zzz.get("subtitle")
        title = zzz.get("title")
        message = f"""<b>Song Shazamed.</b>
<b>Song Name : </b>{title}
<b>Song By : </b>{by}
<u><b>Identified By @DaisyXBot with Friday's song sazam system.
Get Your Friday From</b></u> @FridayOT <b><<u>Also don't forget to Share</b></u> @DaisyXBot <b><<u> and support us..</b></u>
"""
        await event.delete()
        await borg.send_message(
            event.chat_id,
            message,
            parse_mode="HTML",
            file=image,
            force_document=False,
            silent=True,
        )
        os.remove(downloaded_file_name)
    except:
        if xo.get("success") is False:
            errer = xo.get("error")
            ommhg = await event.reply(errer)
            os.remove(downloaded_file_name)
            return
        ommhg = await event.reply("Song Not Found IN Database. Please Try Again.")
        os.remove(downloaded_file_name)
        return
