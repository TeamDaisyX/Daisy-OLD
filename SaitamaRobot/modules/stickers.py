import os
import re
import math
import requests
import urllib.request as urllib

from PIL import Image
from html import escape
from bs4 import BeautifulSoup as bs

from telegram import Update, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram import TelegramError
from telegram.ext import run_async, CallbackContext, CallbackQueryHandler
from telegram.utils.helpers import mention_html

from SaitamaRobot import dispatcher, REDIS
from SaitamaRobot.modules.disable import DisableAbleCommandHandler 


combot_stickers_url = "https://combot.org/telegram/stickers?q="

@run_async
def cb_sticker(update: Update, context: CallbackContext):
    msg = update.effective_message
    split = msg.text.split(' ', 1)
    if len(split) == 1:
        msg.reply_text('Provide Some Name To Search For Packs.')
        return
    text = requests.get(combot_stickers_url + split[1]).text
    soup = bs(text, 'lxml')
    results = soup.find_all("a", {'class': "sticker-pack__btn"})
    titles = soup.find_all("div", "sticker-pack__title")
    if not results:
        msg.reply_text('No Results Found! :(')
        return
    reply = f"Stickers for *{split[1]}*:"
    for result, title in zip(results, titles):
        link = result['href']
        reply += f"\n• [{title.get_text()}]({link})"
    msg.reply_text(reply, parse_mode=ParseMode.MARKDOWN)



@run_async
def addsticker(update, context):
    msg = update.effective_message
    user = update.effective_user
    args = context.args
    packnum = 0
    packname = "a" + str(user.id) + "_by_" + context.bot.username
    packname_found = 0
    max_stickers = 120
    
    
    while packname_found == 0:
        try:
            stickerset = context.bot.get_sticker_set(packname)
            if len(stickerset.stickers) >= max_stickers:
                packnum += 1
                packname = (
                    "a"
                    + str(packnum)
                    + "_"
                    + str(user.id)
                    + "_by_"
                    + context.bot.username
                )
            else:
                packname_found = 1
        except TelegramError as e:
            if e.message == "Stickerset_invalid":
                packname_found = 1
    kangsticker = "kangsticker.png"
    is_animated = False
    file_id = ""

    if msg.reply_to_message:
        if msg.reply_to_message.sticker:
            if msg.reply_to_message.sticker.is_animated:
                is_animated = True
            file_id = msg.reply_to_message.sticker.file_id

        elif msg.reply_to_message.photo:
            file_id = msg.reply_to_message.photo[-1].file_id
        elif msg.reply_to_message.document:
            file_id = msg.reply_to_message.document.file_id
        else:
            msg.reply_text("Yea, I can't kang that.")

        kang_file = context.bot.get_file(file_id)
        if not is_animated:
            kang_file.download("kangsticker.png")
        else:
            kang_file.download("kangsticker.tgs")

        if args:
            sticker_emoji = str(args[0])
        elif msg.reply_to_message.sticker and msg.reply_to_message.sticker.emoji:
            sticker_emoji = msg.reply_to_message.sticker.emoji
        else:
            sticker_emoji = "🙂"
        
        adding_process = msg.reply_text(
                    "<b>Your sticker will be added in few seconds, please wait...</b>",
                    parse_mode=ParseMode.HTML
                    )
        
        if not is_animated:
            try:
                im = Image.open(kangsticker)
                maxsize = (512, 512)
                if (im.width and im.height) < 512:
                    size1 = im.width
                    size2 = im.height
                    if im.width > im.height:
                        scale = 512 / size1
                        size1new = 512
                        size2new = size2 * scale
                    else:
                        scale = 512 / size2
                        size1new = size1 * scale
                        size2new = 512
                    size1new = math.floor(size1new)
                    size2new = math.floor(size2new)
                    sizenew = (size1new, size2new)
                    im = im.resize(sizenew)
                else:
                    im.thumbnail(maxsize)
                if not msg.reply_to_message.sticker:
                    im.save(kangsticker, "PNG")
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    png_sticker=open("kangsticker.png", "rb"),
                    emojis=sticker_emoji,
                )
                edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{packname}"
                            )
                        ]
                    ]
                    )
                adding_process.edit_text(
                    f"<b>Your sticker has been added!</b>"
                    f"\nEmoji Is : {sticker_emoji}",
                    reply_markup=edited_keyboard,
                    parse_mode=ParseMode.HTML
                    )

            except OSError as e:
                
                print(e)
                return

            except TelegramError as e:
                if e.message == "Stickerset_invalid":
                    makepack_internal(
                        update,
                        context,
                        msg,
                        user,
                        sticker_emoji,
                        packname,
                        packnum,
                        png_sticker=open("kangsticker.png", "rb"),
                    )
                    adding_process.delete()
                elif e.message == "Sticker_png_dimensions":
                    im.save(kangsticker, "PNG")
                    adding_process = msg.reply_text(
                        "<b>Your sticker will be added in few seconds, please wait...</b>",
                        parse_mode=ParseMode.HTML
                        )
                    context.bot.add_sticker_to_set(
                        user_id=user.id,
                        name=packname,
                        png_sticker=open("kangsticker.png", "rb"),
                        emojis=sticker_emoji,
                    )
                    edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{packname}"
                                )
                        ]
                    ]
                    )
                    adding_process.edit_text(
                        f"<b>Your sticker has been added!</b>"
                        f"\nEmoji Is : {sticker_emoji}",
                        reply_markup=edited_keyboard,
                        parse_mode=ParseMode.HTML
                        )
                elif e.message == "Invalid sticker emojis":
                    msg.reply_text("Invalid emoji(s).")
                elif e.message == "Stickers_too_much":
                    msg.reply_text("Max packsize reached. Press F to pay respecc.")
                elif e.message == "Internal Server Error: sticker set not found (500)":
                    edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{packname}"
                                )
                        ]
                    ]
                    )
                    msg.reply_text(
                        f"<b>Your sticker has been added!</b>"
                        f"\nEmoji Is : {sticker_emoji}",
                        reply_markup=edited_keyboard,
                        parse_mode=ParseMode.HTML
                        )
                print(e)

        else:
            packname = "animated" + str(user.id) + "_by_" + context.bot.username
            packname_found = 0
            max_stickers = 50
            while packname_found == 0:
                try:
                    stickerset = context.bot.get_sticker_set(packname)
                    if len(stickerset.stickers) >= max_stickers:
                        packnum += 1
                        packname = (
                            "animated"
                            + str(packnum)
                            + "_"
                            + str(user.id)
                            + "_by_"
                            + context.bot.username
                        )
                    else:
                        packname_found = 1
                except TelegramError as e:
                    if e.message == "Stickerset_invalid":
                        packname_found = 1
            try:
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    tgs_sticker=open("kangsticker.tgs", "rb"),
                    emojis=sticker_emoji,
                )
                edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{packname}"
                                )
                        ]
                    ]
                    )
                adding_process.edit_text(
                        f"<b>Your sticker has been added!</b>"
                        f"\nEmoji Is : {sticker_emoji}",
                        reply_markup=edited_keyboard,
                        parse_mode=ParseMode.HTML
                        ) 
            except TelegramError as e:
                if e.message == "Stickerset_invalid":
                    makepack_internal(
                        update,
                        context,
                        msg,
                        user,
                        sticker_emoji,
                        packname,
                        packnum,
                        tgs_sticker=open("kangsticker.tgs", "rb"),
                    )
                    adding_process.delete()
                elif e.message == "Invalid sticker emojis":
                    msg.reply_text("Invalid emoji(s).")
                elif e.message == "Internal Server Error: sticker set not found (500)":
                    edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{packname}"
                                )
                        ]
                    ]
                    )
                    adding_process.edit_text(
                            f"<b>Your sticker has been added!</b>"
                            f"\nEmoji Is : {sticker_emoji}",
                            reply_markup=edited_keyboard,
                            parse_mode=ParseMode.HTML
                            )
                print(e)

    elif args:
        try:
            try:
                urlemoji = msg.text.split(" ")
                png_sticker = urlemoji[1]
                sticker_emoji = urlemoji[2]
            except IndexError:
                sticker_emoji = "🙃"
            urllib.urlretrieve(png_sticker, kangsticker)
            im = Image.open(kangsticker)
            maxsize = (512, 512)
            if (im.width and im.height) < 512:
                size1 = im.width
                size2 = im.height
                if im.width > im.height:
                    scale = 512 / size1
                    size1new = 512
                    size2new = size2 * scale
                else:
                    scale = 512 / size2
                    size1new = size1 * scale
                    size2new = 512
                size1new = math.floor(size1new)
                size2new = math.floor(size2new)
                sizenew = (size1new, size2new)
                im = im.resize(sizenew)
            else:
                im.thumbnail(maxsize)
            im.save(kangsticker, "PNG")
            msg.reply_photo(photo=open("kangsticker.png", "rb"))
            context.bot.add_sticker_to_set(
                user_id=user.id,
                name=packname,
                png_sticker=open("kangsticker.png", "rb"),
                emojis=sticker_emoji,
            )
            edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{packname}"
                                )
                        ]
                    ]
                    )
            adding_process.edit_text(
                        f"<b>Your sticker has been added!</b>"
                        f"\nEmoji Is : {sticker_emoji}",
                        reply_markup=edited_keyboard,
                        parse_mode=ParseMode.HTML
                        )
        except OSError as e:
            msg.reply_text("I can only kang images m8.")
            print(e)
            return
        except TelegramError as e:
            if e.message == "Stickerset_invalid":
                makepack_internal(
                    update,
                    context,
                    msg, 
                    user,
                    sticker_emoji,
                    packname,
                    packnum,
                    png_sticker=open("kangsticker.png", "rb"),
                )
                adding_process.delete()
            elif e.message == "Sticker_png_dimensions":
                im.save(kangsticker, "PNG")
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    png_sticker=open("kangsticker.png", "rb"),
                    emojis=sticker_emoji,
                )
                edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"t.me/addstickers/{packname}"
                                )
                        ]
                    ]
                    )
                adding_process.edit_text(
                            f"<b>Your sticker has been added!</b>"
                            f"\nEmoji Is : {sticker_emoji}",
                            reply_markup=edited_keyboard,
                            parse_mode=ParseMode.HTML
                            )
            elif e.message == "Invalid sticker emojis":
                msg.reply_text("Invalid emoji(s).")
            elif e.message == "Stickers_too_much":
                msg.reply_text("Max packsize reached. Press F to pay respecc.")
            elif e.message == "Internal Server Error: sticker set not found (500)":
                msg.reply_text(
                    f"<b>Your sticker has been added!</b>"
                    f"\nEmoji Is : {sticker_emoji}",
                    reply_markup=edited_keyboard,
                    parse_mode=ParseMode.HTML
                    )
            print(e)
    else:
        packs_text = "*Please reply to a sticker, or image to kang it!*\n"
        if packnum > 0:
            firstpackname = "a" + str(user.id) + "_by_" + context.bot.username
            for i in range(0, packnum + 1):
                if i == 0:
                    packs = f"t.me/addstickers/{firstpackname}"
                else:
                    packs = f"t.me/addstickers/{packname}"
        else:
            packs = f"t.me/addstickers/{packname}"
        
        edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="View Pack", url=f"{packs}"
                                )
                        ]
                    ]
                    )
        msg.reply_text(packs_text   ,
                       reply_markup=edited_keyboard,
                       parse_mode=ParseMode.MARKDOWN
                       )
    if os.path.isfile("kangsticker.png"):
        os.remove("kangsticker.png")
    elif os.path.isfile("kangsticker.tgs"):
        os.remove("kangsticker.tgs")


def makepack_internal(
    update,
    context,
    msg,
    user,
    emoji,
    packname,
    packnum,
    png_sticker=None,
    tgs_sticker=None,
):
    name = user.first_name
    name = name[:50]
    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                                text="View Pack", url=f"{packname}"
                                )
                ]
            ]
            )
    try:
        extra_version = ""
        if packnum > 0:
            extra_version = " " + str(packnum)
        if png_sticker:
            sticker_pack_name = f"{name}'s stic-pack (@{context.bot.username})" + extra_version
            success = context.bot.create_new_sticker_set(
                user.id,
                packname,
                sticker_pack_name,
                png_sticker=png_sticker,
                emojis=emoji,
            )
        if tgs_sticker:
            sticker_pack_name = f"{name}'s ani-pack (@{context.bot.username})" + extra_version
            success = context.bot.create_new_sticker_set(
                user.id,
                packname,
                sticker_pack_name,
                tgs_sticker=tgs_sticker,
                emojis=emoji,
            )

    except TelegramError as e:
        print(e)
        if e.message == "Sticker set name is already occupied":
            msg.reply_text(
                "<b>Your Sticker Pack is already created!</b>"
                "\n\nYou can now reply to images, stickers and animated sticker with /addsticker to add them to your pack"
                "\n\n<b>Send /findpacks to find any sticker pack.</b>",
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML 
            )
        elif e.message == "Peer_id_invalid" or "bot was blocked by the user":
            msg.reply_text(
                f"{context.bot.first_name} was blocked by you.", 
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Unblock", url=f"t.me/{context.bot.username}"
                            )
                        ]
                    ]
                ),
            )
        elif e.message == "Internal Server Error: created sticker set not found (500)":
            msg.reply_text(
                "<b>Your Sticker Pack has been created!</b>"
                "\n\nYou can now reply to images, stickers and animated sticker with /addsticker to add them to your pack"
                "\n\n<b>Send /findpacks to find sticker pack.</b>",
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML
            )
        return

    if success:
        msg.reply_text(
                "<b>Your Sticker Pack has been created!</b>"
                "\n\nYou can now reply to images, stickers and animated sticker with /addsticker to add them to your pack"
                "\n\n<b>Send /findpacks to find sticker pack.</b>",
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML
            )
    else:
        msg.reply_text("Failed to create sticker pack. Possibly due to blek mejik.")

@run_async
def getsticker(update, context):
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        context.bot.sendChatAction(chat_id, "typing")
        update.effective_message.reply_text(
            "Hello"
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", Please check the file you requested below."
            "\nPlease use this feature wisely!",
            parse_mode=ParseMode.HTML,
        )
        context.bot.sendChatAction(chat_id, "upload_document")
        file_id = msg.reply_to_message.sticker.file_id
        newFile = context.bot.get_file(file_id)
        newFile.download("sticker.png")
        context.bot.sendDocument(chat_id, document=open("sticker.png", "rb"))
        context.bot.sendChatAction(chat_id, "upload_photo")
        context.bot.send_photo(chat_id, photo=open("sticker.png", "rb"))

    else:
        context.bot.sendChatAction(chat_id, "typing")
        update.effective_message.reply_text(
            "Hello"
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", Please reply to sticker message to get sticker image",
            parse_mode=ParseMode.HTML,
        )


@run_async
def stickerid(update, context):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        update.effective_message.reply_text(
            "Hello "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", The sticker id you are replying is :\n <code>"
            + escape(msg.reply_to_message.sticker.file_id)
            + "</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text(
            "Hello "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", Please reply to sticker message to get id sticker",
            parse_mode=ParseMode.HTML,
        )

@run_async
def delsticker(update, context):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        context.bot.delete_sticker_from_set(file_id)
        msg.reply_text(
            "Deleted!"
        )
    else:
        update.effective_message.reply_text(
            "Please reply to sticker message to del sticker"
        )
    
@run_async
def add_fvrtsticker(update, context):
    bot = context.bot
    message = update.effective_message  
    chat = update.effective_chat 
    user = update.effective_user 
    args = context.args
    query = " ".join(args)
    if message.reply_to_message and message.reply_to_message.sticker:
        get_s_name = message.reply_to_message.sticker.set_name
        if not query:
            get_s_name_title = get_s_name
        else:
            get_s_name_title = query
        if get_s_name is None:
            message.reply_text(
                "Sticker is invalid!"
            )
        sticker_url = f"https://t.me/addstickers/{get_s_name}"
        sticker_m = "<a href='{}'>{}</a>".format(sticker_url, get_s_name_title)
        check_pack = REDIS.hexists(f'fvrt_stickers2_{user.id}', get_s_name_title)
        if check_pack == False:
            REDIS.hset(f'fvrt_stickers2_{user.id}', get_s_name_title, sticker_m)
            message.reply_text(
                f"<code>{sticker_m}</code> has been succesfully added into your favorite sticker packs list!",
                parse_mode=ParseMode.HTML
            )
        else:
            message.reply_text(
                f"<code>{sticker_m}</code> is already exist in your favorite sticker packs list!",
                parse_mode=ParseMode.HTML
            )
        
    else:
        message.reply_text(
            'Reply to any sticker!'
        )  

@run_async
def list_fvrtsticker(update, context): 
    message = update.effective_message  
    chat = update.effective_chat 
    user = update.effective_user 
    fvrt_stickers_list = REDIS.hvals(f'fvrt_stickers2_{user.id}')
    fvrt_stickers_list.sort()
    fvrt_stickers_list = "\n• ".join(fvrt_stickers_list)
    if fvrt_stickers_list: 
        message.reply_text(
            "{}'s favorite sticker packs:\n• {}".format(user.first_name,
                                                  fvrt_stickers_list),
            parse_mode=ParseMode.HTML
        ) 
    else:
        message.reply_text(
            "You haven't added any sticker yet."
        )

@run_async
def remove_fvrtsticker(update, context): 
    message = update.effective_message  
    chat = update.effective_chat 
    user = update.effective_user 
    args = context.args
    del_stick = " ".join(args)
    if not del_stick:
        message.reply_text("Please give a your favorite sticker pack name to remove from your list.")
        return
    del_check = REDIS.hexists(f'fvrt_stickers2_{user.id}', del_stick)
    if not del_check == False:
        REDIS.hdel(f'fvrt_stickers2_{user.id}',del_stick)
        message.reply_text(
            f"<code>{del_stick}</code> has been succesfully deleted from your list.",
            parse_mode=ParseMode.HTML
        )
    else:
        message.reply_text(
            f"<code>{del_stick}</code> doesn't exist in your favorite sticker pack list.",
            parse_mode=ParseMode.HTML
        )
        
__help__ = """
Stickers made easy with stickers module!

- /findsticker: Find stickers for given term on combot sticker catalogue 

- /addsticker: Reply to a sticker to add it to your pack.
- /delsticker: Reply to your anime exist sticker to your pack to delete it.
- /stickerid: Reply to a sticker to me to tell you its file ID.
- /getsticker: Reply to a sticker to me to upload its raw PNG file.
- /addfsticker or /afs <custom name>: Reply to a sticker to add it into your favorite pack list.
- /myfsticker or /mfs: Get list of your favorite packs.
- /removefsticker or /rfs <custom name>: Reply to a sticker to remove it into your favorite pack list.

*Example:* `/addfsticker my cool pack`
"""

__mod_name__ = "Stickers"
KANG_HANDLER = DisableAbleCommandHandler(["addsticker", "kang", "steal"], addsticker, pass_args=True)
DEL_HANDLER = DisableAbleCommandHandler("delsticker", delsticker)
STICKERID_HANDLER = DisableAbleCommandHandler("stickerid", stickerid)
ADD_FSTICKER_HANDLER = DisableAbleCommandHandler(["addfsticker","afs"], add_fvrtsticker, pass_args=True)
REMOVE_FSTICKER_HANDLER = DisableAbleCommandHandler(["removefsticker","rfs"], remove_fvrtsticker, pass_args=True)
MY_FSTICKERS_HANDLER = DisableAbleCommandHandler(["myfsticker","mfs"], list_fvrtsticker)
GETSTICKER_HANDLER = DisableAbleCommandHandler("getsticker", getsticker)
FIND_STICKERS_HANDLER = DisableAbleCommandHandler("findpacks", cb_sticker)

dispatcher.add_handler(KANG_HANDLER)
dispatcher.add_handler(DEL_HANDLER)
dispatcher.add_handler(STICKERID_HANDLER)
dispatcher.add_handler(ADD_FSTICKER_HANDLER)
dispatcher.add_handler(REMOVE_FSTICKER_HANDLER)
dispatcher.add_handler(MY_FSTICKERS_HANDLER)
dispatcher.add_handler(GETSTICKER_HANDLER)
dispatcher.add_handler(FIND_STICKERS_HANDLER)