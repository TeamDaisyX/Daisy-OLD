import os

import cloudmersive_ocr_api_client
from cloudmersive_ocr_api_client.rest import ApiException
from pymongo import MongoClient
from telethon import *
from telethon.tl import functions, types
from telethon.tl.types import *

from DaisyX import *
from DaisyX import telethn as tbot
from DaisyX.events import register

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["missjuliarobot"]
approved_users = db.approve

configuration = cloudmersive_ocr_api_client.Configuration()
configuration.api_key["Apikey"] = VIRUS_API_KEY
api_instance = cloudmersive_ocr_api_client.ImageOcrApi(
    cloudmersive_ocr_api_client.ApiClient(configuration)
)


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await tbot.get_peer_id(user)
        ps = (
            await tbot(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None


@register(pattern="^/img2text (.*)")
async def parse_ocr_space_api(event):
    if event.fwd_from:
        return
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    gg = await event.reply("Processing ...")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    lang_code = event.pattern_match.group(1)
    language = lang_code
    downloaded_file_name = await tbot.download_media(
        await event.get_reply_message(), TEMP_DOWNLOAD_DIRECTORY
    )
    try:
        api_response = api_instance.image_ocr_post(
            downloaded_file_name, language=language
        )
    except ApiException as e:
        print(e)
        os.remove(downloaded_file_name)
        await gg.edit("Some error occurred.")
        return
    await gg.edit("{}".format(api_response.text_result))
    os.remove(downloaded_file_name)


@register(pattern="^/img2textlang")
async def get_ocr_languages(event):
    if event.fwd_from:
        return
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]
    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        elif event.chat_id == iid and event.sender_id == userss:
            pass
        else:
            return
    languages = """**These are the available languages 👇**\n
ENG (English)
ARA (Arabic)
ZHO (Chinese - Simplified)
ZHO-HANT (Chinese - Traditional)
ASM (Assamese)
AFR (Afrikaans)
AMH (Amharic)
AZE (Azerbaijani)
AZE-CYRL (Azerbaijani - Cyrillic)
BEL (Belarusian)
BEN (Bengali)
BOD (Tibetan)
BOS (Bosnian)
BUL (Bulgarian)
CAT (Catalan; Valencian)
CEB (Cebuano)
CES (Czech)
CHR (Cherokee)
CYM (Welsh)
DAN (Danish)
DEU (German)
DZO (Dzongkha)
ELL (Greek)
ENM (Archaic/Middle English)
EPO (Esperanto)
EST (Estonian)
EUS (Basque)
FAS (Persian)
FIN (Finnish)
FRA (French)
FRK (Frankish)
FRM (Middle-French)
GLE (Irish)
GLG (Galician)
GRC (Ancient Greek)
HAT (Hatian)
HEB (Hebrew)
HIN (Hindi)
HRV (Croatian)
HUN (Hungarian)
IKU (Inuktitut)
IND (Indonesian)
ISL (Icelandic)
ITA (Italian)
ITA-OLD (Old - Italian)
JAV (Javanese)
JPN (Japanese)
KAN (Kannada)
KAT (Georgian)
KAT-OLD (Old-Georgian)
KAZ (Kazakh)
KHM (Central Khmer)
KIR (Kirghiz)
KOR (Korean)
KUR (Kurdish)
LAO (Lao)
LAT (Latin)
LAV (Latvian)
LIT (Lithuanian)
MAL (Malayalam)
MAR (Marathi)
MKD (Macedonian)
MLT (Maltese)
MSA (Malay)
MYA (Burmese)
NEP (Nepali)
NLD (Dutch)
NOR (Norwegian)
ORI (Oriya)
PAN (Panjabi)
POL (Polish)
POR (Portuguese)
PUS (Pushto)
RON (Romanian)
RUS (Russian)
SAN (Sanskrit)
SIN (Sinhala)
SLK (Slovak)
SLV (Slovenian)
SPA (Spanish)
SPA-OLD (Old Spanish)
SQI (Albanian)
SRP (Serbian)
SRP-LAT (Latin Serbian)
SWA (Swahili)
SWE (Swedish)
SYR (Syriac)
TAM (Tamil)
TEL (Telugu)
TGK (Tajik)
TGL (Tagalog)
THA (Thai)
TIR (Tigrinya)
TUR (Turkish)
UIG (Uighur)
UKR (Ukrainian)
URD (Urdu)
UZB (Uzbek)
UZB-CYR (Cyrillic Uzbek)
VIE (Vietnamese)
YID (Yiddish) (optional)
    """
    await event.reply(languages)
