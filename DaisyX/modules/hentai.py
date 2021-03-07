# Kanged from Hackfreaks.. All credits to them..

from functools import wraps

import nekos
from telegram import ParseMode
from telegram.ext import CommandHandler
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import mention_html

import DaisyX.modules.sql.hentai_sql as sql
from DaisyX import EVENT_LOGS, dispatcher
from DaisyX.modules.disable import DisableAbleCommandHandler
from DaisyX.modules.helper_funcs.filters import CustomFilters


def hentai_supplier(func):
    @wraps(func)
    def allowed_chat(update, context, *args, **kwargs):
        chat = update.effective_chat
        isAllowed = sql.isAdded(str(chat.id))
        if isAllowed or chat.type == "private":
            sql.addedChat(str(chat.id))
            return func(update, context, *args, **kwargs)

        elif not isAllowed:
            pass

        elif DEL_CMDS and " " not in update.effective_message.text:
            update.effective_message.delete()

        else:
            update.effective_message.reply_text(
                "As this module contain explicit things. Your group should be private and approoved by us, if you want ask for approval [Here](https://telegram.dog/inukaasith) or [Here](https://telegram.dog/infinityje)"
            )

    return allowed_chat


@run_async
def addhentai(update, context):
    args = context.args
    if args and len(args) == 1:
        chat_id = str(args[0])
        del args[0]
        try:
            banner = update.effective_user
            context.bot.send_message(
                EVENT_LOGS,
                "<b>Chat Added for Hentai Supplier</b>"
                "\n#Added to Hentai"
                "\n#Successfull #EnjoyMore"
                "\n<b>Status:</b> <code>Added</code>"
                "\n<b>Sudo Admin:</b> {}"
                "\n<b>ID:</b> <code>{}</code>".format(
                    mention_html(banner.id, banner.first_name), chat_id
                ),
                parse_mode=ParseMode.HTML,
            )
            sql.addedChat(chat_id)
            update.effective_message.reply_text(
                "Chat has been successfully added for Hentai Supplier!"
            )
        except:
            update.effective_message.reply_text("Error adding chat!")
    else:
        update.effective_message.reply_text("Give me a valid chat id!")


@run_async
def removehentai(update, context):
    args = context.args
    if args and len(args) == 1:
        chat_id = str(args[0])
        del args[0]
        try:
            banner = update.effective_user
            context.bot.send_message(
                EVENT_LOGS,
                "<b>Regression of Chat for Hentai Supplier</b>"
                "\n#Removed Hentai"
                "\n#REMOVED #BYE"
                "\n<b>Status:</b> <code>Removed</code>"
                "\n<b>Sudo Admin:</b> {}"
                "\n<b>ID:</b> <code>{}</code>".format(
                    mention_html(banner.id, banner.first_name), chat_id
                ),
                parse_mode=ParseMode.HTML,
            )
            sql.removedChat(chat_id)
            update.effective_message.reply_text(
                "Chat has been successfully removed for Hentai Supplier"
            )
        except:
            update.effective_message.reply_text("Error removing chat!")
    else:
        update.effective_message.reply_text("Give me a valid chat id!")


# Begin hentai functions ....


@hentai_supplier
@run_async
def pussy(update, context):
    update.message.reply_photo(nekos.img("pussy_jpg"))


@hentai_supplier
@run_async
def hentaig(update, context):
    update.message.reply_video(nekos.img("random_hentai_gif"))


@hentai_supplier
@run_async
def neko(update, context):
    update.message.reply_document(nekos.img("neko"))


@hentai_supplier
@run_async
def feet(update, context):
    update.message.reply_photo(nekos.img("feet"))


@hentai_supplier
@run_async
def yuri(update, context):
    update.message.reply_photo(nekos.img("yuri"))


@hentai_supplier
@run_async
def trap(update, context):
    update.message.reply_photo(nekos.img("trap"))


@hentai_supplier
@run_async
def futanari(update, context):
    update.message.reply_photo(nekos.img("futanari"))


@hentai_supplier
@run_async
def hololewd(update, context):
    update.message.reply_photo(nekos.img("hololewd"))


@hentai_supplier
@run_async
def lewdkemo(update, context):
    update.message.reply_photo(nekos.img("lewdkemo"))


@hentai_supplier
@run_async
def solog(update, context):
    update.message.reply_video(nekos.img("solog"))


@hentai_supplier
@run_async
def feetg(update, context):
    update.message.reply_video(nekos.img("feetg"))


@hentai_supplier
@run_async
def cumg(update, context):
    update.message.reply_video(nekos.img("cum"))


@hentai_supplier
@run_async
def erokemo(update, context):
    update.message.reply_photo(nekos.img("erokemo"))


@hentai_supplier
@run_async
def lesbian(update, context):
    update.message.reply_photo(nekos.img("les"))


@hentai_supplier
@run_async
def wallpaper(update, context):
    update.message.reply_document(nekos.img("wallpaper"))


@hentai_supplier
@run_async
def lewdk(update, context):
    update.message.reply_photo(nekos.img("lewdk"))


@hentai_supplier
@run_async
def ngif(update, context):
    update.message.reply_video(nekos.img("ngif"))


@hentai_supplier
@run_async
def tickle(update, context):
    update.message.reply_photo(nekos.img("tickle"))


@hentai_supplier
@run_async
def lewd(update, context):
    update.message.reply_photo(nekos.img("lewd"))


@hentai_supplier
@run_async
def feed(update, context):
    update.message.reply_photo(nekos.img("feed"))


@hentai_supplier
@run_async
def eroyuri(update, context):
    update.message.reply_photo(nekos.img("eroyuri"))


@hentai_supplier
@run_async
def eron(update, context):
    update.message.reply_photo(nekos.img("eron"))


@hentai_supplier
@run_async
def cum(update, context):
    update.message.reply_photo(nekos.img("cum_jpg"))


@hentai_supplier
@run_async
def bjgif(update, context):
    update.message.reply_video(nekos.img("bj"))


@hentai_supplier
@run_async
def bj(update, context):
    update.message.reply_photo(nekos.img("blowjob"))


@hentai_supplier
@run_async
def nekonsfw(update, context):
    update.message.reply_video(nekos.img("nsfw_neko_gif"))


@hentai_supplier
@run_async
def solo(update, context):
    update.message.reply_photo(nekos.img("solo"))


@hentai_supplier
@run_async
def kemonomimi(update, context):
    update.message.reply_photo(nekos.img("kemonomimi"))


@hentai_supplier
@run_async
def pokeg(update, context):
    update.message.reply_video(nekos.img("poke"))


@hentai_supplier
@run_async
def analg(update, context):
    update.message.reply_video(nekos.img("anal"))


@hentai_supplier
@run_async
def hentai(update, context):
    update.message.reply_photo(nekos.img("hentai"))


@hentai_supplier
@run_async
def erofeet(update, context):
    update.message.reply_photo(nekos.img("erofeet"))


@hentai_supplier
@run_async
def holo(update, context):
    update.message.reply_photo(nekos.img("holo"))


@hentai_supplier
@run_async
def pussyg(update, context):
    update.message.reply_video(nekos.img("pussy"))


@hentai_supplier
@run_async
def tits(update, context):
    update.message.reply_photo(nekos.img("tits"))


@hentai_supplier
@run_async
def holoero(update, context):
    update.message.reply_photo(nekos.img("holoero"))


@hentai_supplier
@run_async
def classic(update, context):
    update.message.reply_video(nekos.img("classic"))


@hentai_supplier
@run_async
def kuni(update, context):
    update.message.reply_video(nekos.img("kuni"))


ADDHENTAI_HANDLER = CommandHandler(
    "addhentai", addhentai, pass_args=True, filters=CustomFilters.sudo_filter
)
REMOVEHENTAI_HANDLER = CommandHandler(
    "removehentai", removehentai, pass_args=True, filters=CustomFilters.sudo_filter
)

PUSSY_HANDLER = DisableAbleCommandHandler("pussy", pussy)
HENTAIG_HANDLER = DisableAbleCommandHandler("hentaigif", hentaig)
NEKO_HANDLER = DisableAbleCommandHandler("neko", neko)
FEET_HANDLER = DisableAbleCommandHandler("feet", feet)
YURI_HANDLER = DisableAbleCommandHandler("yuri", yuri)
TRAP_HANDLER = DisableAbleCommandHandler("trap", trap)
FUTANARI_HANDLER = DisableAbleCommandHandler("futanari", futanari)
HOLOLEWD_HANDLER = DisableAbleCommandHandler("hololewd", hololewd)
LEWDKEMO_HANDLER = DisableAbleCommandHandler("lewdkemo", lewdkemo)
SOLOG_HANDLER = DisableAbleCommandHandler("sologif", solog)
FEETG_HANDLER = DisableAbleCommandHandler("feetgif", feetg)
CUMG_HANDLER = DisableAbleCommandHandler("cumgif", cumg)
EROKEMO_HANDLER = DisableAbleCommandHandler("erokemo", erokemo)
LESBIAN_HANDLER = DisableAbleCommandHandler("lesbian", lesbian)
WALLPAPER_HANDLER = DisableAbleCommandHandler("walls", wallpaper)
LEWDK_HANDLER = DisableAbleCommandHandler("lewdk", lewdk)
NGIF_HANDLER = DisableAbleCommandHandler("ngif", ngif)
TICKLE_HANDLER = DisableAbleCommandHandler("tickle", tickle)
LEWD_HANDLER = DisableAbleCommandHandler("lewd", lewd)
FEED_HANDLER = DisableAbleCommandHandler("feed", feed)
EROYURI_HANDLER = DisableAbleCommandHandler("eroyuri", eroyuri)
ERON_HANDLER = DisableAbleCommandHandler("eron", eron)
CUM_HANDLER = DisableAbleCommandHandler("cum", cum)
BJGIF_HANDLER = DisableAbleCommandHandler("bjgif", bjgif)
BJ_HANDLER = DisableAbleCommandHandler("bj", bj)
NEKONSFW_HANDLER = DisableAbleCommandHandler("nekonsfw", nekonsfw)
SOLO_HANDLER = DisableAbleCommandHandler("solo", solo)
KEMONOMIMI_HANDLER = DisableAbleCommandHandler("kemonomimi", kemonomimi)
POKEG_HANDLER = DisableAbleCommandHandler("pokegif", pokeg)
ANALG_HANDLER = DisableAbleCommandHandler("analgif", analg)
HENTAI_HANDLER = DisableAbleCommandHandler("hentai", hentai)
EROFEET_HANDLER = DisableAbleCommandHandler("erofeet", erofeet)
HOLO_HANDLER = DisableAbleCommandHandler("holo", holo)
PUSSYG_HANDLER = DisableAbleCommandHandler("pussygif", pussyg)
TITS_HANDLER = DisableAbleCommandHandler("boobs", tits)
HOLOERO_HANDLER = DisableAbleCommandHandler("holoero", holoero)
CLASSIC_HANDLER = DisableAbleCommandHandler("classic", classic)
KUNI_HANDLER = DisableAbleCommandHandler("kuni", kuni)


dispatcher.add_handler(ADDHENTAI_HANDLER)
dispatcher.add_handler(REMOVEHENTAI_HANDLER)

dispatcher.add_handler(PUSSY_HANDLER)
dispatcher.add_handler(HENTAIG_HANDLER)
dispatcher.add_handler(NEKO_HANDLER)
dispatcher.add_handler(FEET_HANDLER)
dispatcher.add_handler(YURI_HANDLER)
dispatcher.add_handler(TRAP_HANDLER)
dispatcher.add_handler(FUTANARI_HANDLER)
dispatcher.add_handler(HOLOLEWD_HANDLER)
dispatcher.add_handler(LEWDKEMO_HANDLER)
dispatcher.add_handler(SOLOG_HANDLER)
dispatcher.add_handler(FEETG_HANDLER)
dispatcher.add_handler(CUMG_HANDLER)
dispatcher.add_handler(EROKEMO_HANDLER)
dispatcher.add_handler(LESBIAN_HANDLER)
dispatcher.add_handler(WALLPAPER_HANDLER)
dispatcher.add_handler(LEWDK_HANDLER)
dispatcher.add_handler(NGIF_HANDLER)
dispatcher.add_handler(TICKLE_HANDLER)
dispatcher.add_handler(LEWD_HANDLER)
dispatcher.add_handler(FEED_HANDLER)
dispatcher.add_handler(EROYURI_HANDLER)
dispatcher.add_handler(ERON_HANDLER)
dispatcher.add_handler(CUM_HANDLER)
dispatcher.add_handler(BJGIF_HANDLER)
dispatcher.add_handler(BJ_HANDLER)
dispatcher.add_handler(NEKONSFW_HANDLER)
dispatcher.add_handler(SOLO_HANDLER)
dispatcher.add_handler(KEMONOMIMI_HANDLER)
dispatcher.add_handler(POKEG_HANDLER)
dispatcher.add_handler(ANALG_HANDLER)
dispatcher.add_handler(HENTAI_HANDLER)
dispatcher.add_handler(EROFEET_HANDLER)
dispatcher.add_handler(HOLO_HANDLER)
dispatcher.add_handler(PUSSYG_HANDLER)
dispatcher.add_handler(TITS_HANDLER)
dispatcher.add_handler(HOLOERO_HANDLER)
dispatcher.add_handler(CLASSIC_HANDLER)
dispatcher.add_handler(KUNI_HANDLER)
