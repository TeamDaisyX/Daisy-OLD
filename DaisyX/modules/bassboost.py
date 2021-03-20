import asyncio
import io
import math
import os

import numpy as np
from pydub import AudioSegment
from telethon import types
from telethon import events
from DaisyX.services.telethon import tbot
from DaisyX.function.telethonbasics import is_admin
from DaisyX import BOT_ID

@tbot.on(events.NewMessage(pattern="/bassboost (.*)"))
async def __(message):
    if not message.is_group:
        await message.reply("To reduce server overloading. We restricted using this command only in groups")
        return
    if not await is_admin(message, BOT_ID): 
        await message.reply("`I Should Be Admin To Do This!`")
        return
    if await is_admin(message, message.message.sender_id): 
      v = False
      accentuate_db = 40
      reply = await message.get_reply_message()
      if not reply:
          await message.reply("Can You Reply To A MSG :?")
          return
      if message.pattern_match.group(1):
          ar = message.pattern_match.group(1)
          try:
              int(ar)
              if int(ar) >= 2 and int(ar) <= 100:
                  accentuate_db = int(ar)
              else:
                  await message.reply("`BassBost Level Should Be From 2 to 100 Only.`")
                  return
          except Exception as exx:
              await message.reply("`SomeThing Went Wrong..` \n**Error:** " + str(exx))
              return
      else:
          accentuate_db = 2
      await message.reply("`Downloading This File...`")
      fname = await tbot.download_media(message=reply.media)
      await message.edit("`BassBoosting In Progress..`")
      if fname.endswith(".oga") or fname.endswith(".ogg"):
          v = True
          audio = AudioSegment.from_file(fname)
      elif fname.endswith(".mp3") or fname.endswith(".m4a") or fname.endswith(".wav"):
          audio = AudioSegment.from_file(fname)
      else:
          await message.edit(
              "`This Format is Not Supported Yet` \n**Currently Supported :** `mp3, m4a and wav.`"
          )
          os.remove(fname)
          return
      sample_track = list(audio.get_array_of_samples())
      await asyncio.sleep(0.3)
      est_mean = np.mean(sample_track)
      await asyncio.sleep(0.3)
      est_std = 3 * np.std(sample_track) / (math.sqrt(2))
      await asyncio.sleep(0.3)
      bass_factor = int(round((est_std - est_mean) * 0.005))
      await asyncio.sleep(5)
      attenuate_db = 0
      filtered = audio.low_pass_filter(bass_factor)
      await asyncio.sleep(5)
      out = (audio - attenuate_db).overlay(filtered + accentuate_db)
      await asyncio.sleep(6)
      m = io.BytesIO()
      if v:
          m.name = "voice.ogg"
          out.split_to_mono()
          await message.edit("`Now Exporting...`")
          await asyncio.sleep(0.3)
          out.export(m, format="ogg", bitrate="64k", codec="libopus")
          await message.edit("`Process Completed. Uploading Now Here..`")
          await borg.send_file(
              message.to_id,
              m,
              reply_to=reply.id,
              voice_note=True,
              caption="Bass Boosted, \nDone By @DaisySupport_Official",
          )
          os.remove(m)
      else:
          m.name = "BassBoosted.mp3"
          await message.edit("`Now Exporting...`")
          await asyncio.sleep(0.3)
          out.export(m, format="mp3")
          await message.edit("`Process Completed. Uploading Now Here..`")
          await tbot.send_file(
              message.to_id,
              m,
              reply_to=reply.id,
              attributes=[
                  types.DocumentAttributeAudio(
                      duration=reply.document.attributes[0].duration,
                      title=f"BassBoost {str(accentuate_db)}lvl",
                      performer="BassBoost",
                  )
              ],
              caption="Bass Boosted, \nDone By @DaisySupport_Official",
          )
          os.remove(m)
      await message.delete()
      os.remove(fname)
      
    else:
        await event.reply("`You Should Be Admin To Do This!`")
        return      
      
