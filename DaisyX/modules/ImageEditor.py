# By @TroJanzHEX
# Rewrite to DaisyX by @InukaASiTH


from DaisyX.Addons.ImgEditor.edit_1 import (  # pylint:disable=import-error
    bright,
    mix,
    g_blur,
    normal_blur,
    black_white,
    box_blur,
)
from DaisyX.Addons.ImgEditor.edit_2 import (  # pylint:disable=import-error
    circle_with_bg,
    circle_without_bg,
    sticker,
    edge_curved,
    contrast,
    sepia_mode,
    pencil,
    cartoon,
)
from DaisyX.Addons.ImgEditor.edit_3 import (  # pylint:disable=import-error
    green_border,
    blue_border,
    black_border,
    red_border,
)
from DaisyX.Addons.ImgEditor.edit_4 import (  # pylint:disable=import-error
    rotate_90,
    rotate_180,
    rotate_270,
    inverted,
    round_sticker,
    removebg_white,
    removebg_plain,
    removebg_sticker,
)
from DaisyX.Addons.ImgEditor.edit_5 import (  # pylint:disable=import-error
    normalglitch_1,
    normalglitch_2,
    normalglitch_3,
    normalglitch_4,
    normalglitch_5,
    scanlineglitch_1,
    scanlineglitch_2,
    scanlineglitch_3,
    scanlineglitch_4,
    scanlineglitch_5,
)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from DaisyX.services.pyrogram import pbot as Client 
from pyrogram import filters

@Client.on_message(filters.command(["edit", "editimage","editor"]))
async def photo(client: Client, message: Message):
    replied = message.reply_to_message
    if not replied:
        await edit_or_reply(message, text='Reply to a photo to open image editor')
        return
    if not replied.photo:
        await edit_or_reply(message, text='Reply to a photo to open image editor')
        return
    try:
        await client.send_message(
            chat_id=message.chat.id,
            text="Select your required mode from below!\n **Powered by @DaisySupport_Official**ㅤㅤ",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="BRIGHT", callback_data="bright"),
                        InlineKeyboardButton(text="MIXED", callback_data="mix"),
                        InlineKeyboardButton(text="B&W", callback_data="b|w"),
                    ],
                    [
                        InlineKeyboardButton(text="CIRCLE", callback_data="circle"),
                        InlineKeyboardButton(text="BLUR", callback_data="blur"),
                        InlineKeyboardButton(text="BORDER", callback_data="border"),
                    ],
                    [
                        InlineKeyboardButton(text="STICKER", callback_data="stick"),
                        InlineKeyboardButton(text="ROTATE", callback_data="rotate"),
                        InlineKeyboardButton(text="CONTRAST", callback_data="contrast"),
                    ],
                    [
                        InlineKeyboardButton(text="SEPIA", callback_data="sepia"),
                        InlineKeyboardButton(text="PENCIL", callback_data="pencil"),
                        InlineKeyboardButton(text="CARTOON", callback_data="cartoon"),
                    ],
                    [
                        InlineKeyboardButton(text="INVERT", callback_data="inverted"),
                        InlineKeyboardButton(text="GLITCH", callback_data="glitch"),
                        InlineKeyboardButton(
                            text="REMOVE BG", callback_data="removebg"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="CLOSE", callback_data="close_e"),
                    ],
                ]
            ),
            reply_to_message_id,
        )
    except Exception as e:
        print("photomarkup error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_text("Something went wrong!", quote=True)
            except Exception:
                return





@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "removebg":
        await query.message.edit_text(
            "**Select required mode**ㅤㅤㅤㅤ",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="WITH WHITE BG", callback_data="rmbgwhite"
                        ),
                        InlineKeyboardButton(
                            text="WITHOUT BG", callback_data="rmbgplain"
                        ),
                    ],
                    [InlineKeyboardButton(text="STICKER", callback_data="rmbgsticker")],
                ]
            ),
        )
    elif query.data == "stick":
        await query.message.edit(
            "**Select a Type**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Normal", callback_data="stkr"),
                        InlineKeyboardButton(
                            text="Edge Curved", callback_data="cur_ved"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="Circle", callback_data="circle_sticker"
                        )
                    ],
                ]
            ),
        )
    elif query.data == "rotate":
        await query.message.edit_text(
            "**Select the Degree**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="180", callback_data="180"),
                        InlineKeyboardButton(text="90", callback_data="90"),
                    ],
                    [InlineKeyboardButton(text="270", callback_data="270")],
                ]
            ),
        )
    elif query.data == "glitch":
        await query.message.edit_text(
            "**Select required mode**ㅤㅤㅤㅤ",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="NORMAL", callback_data="normalglitch"
                        ),
                        InlineKeyboardButton(
                            text="SCAN LINES", callback_data="scanlineglitch"
                        ),
                    ]
                ]
            ),
        )
    elif query.data == "normalglitch":
        await query.message.edit_text(
            "**Select Glitch power level**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="1", callback_data="normalglitch1"),
                        InlineKeyboardButton(text="2", callback_data="normalglitch2"),
                        InlineKeyboardButton(text="3", callback_data="normalglitch3"),
                    ],
                    [
                        InlineKeyboardButton(text="4", callback_data="normalglitch4"),
                        InlineKeyboardButton(text="5", callback_data="normalglitch5"),
                    ],
                ]
            ),
        )
    elif query.data == "scanlineglitch":
        await query.message.edit_text(
            "**Select Glitch power level**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="1", callback_data="scanlineglitch1"),
                        InlineKeyboardButton(text="2", callback_data="scanlineglitch2"),
                        InlineKeyboardButton(text="3", callback_data="scanlineglitch3"),
                    ],
                    [
                        InlineKeyboardButton(text="4", callback_data="scanlineglitch4"),
                        InlineKeyboardButton(text="5", callback_data="scanlineglitch5"),
                    ],
                ]
            ),
        )
    elif query.data == "blur":
        await query.message.edit(
            "**Select a Type**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="box", callback_data="box"),
                        InlineKeyboardButton(text="normal", callback_data="normal"),
                    ],
                    [InlineKeyboardButton(text="Gaussian", callback_data="gas")],
                ]
            ),
        )
    elif query.data == "circle":
        await query.message.edit_text(
            "**Select required mode**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="WITH BG", callback_data="circlewithbg"
                        ),
                        InlineKeyboardButton(
                            text="WITHOUT BG", callback_data="circlewithoutbg"
                        ),
                    ]
                ]
            ),
        )
    elif query.data == "border":
        await query.message.edit(
            "**Select Border**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🔴 RED 🔴", callback_data="red"),
                        InlineKeyboardButton(text="🟢 Green 🟢", callback_data="green"),
                    ],
                    [
                        InlineKeyboardButton(text="⚫ Black ⚫", callback_data="black"),
                        InlineKeyboardButton(text="🔵 Blue 🔵", callback_data="blue"),
                    ],
                ]
            ),
        )
        
    if query.data not in [
        "removebg",
        "stick",
        "rotate",
        "glitch",
        "normalglitch",
        "scanlineglitch",
        "blur",
        "circle",
        "border",
    ]:
    
        #await query.message.delete()
        if query.data == "bright":
            await bright(client, query.message)

        elif query.data == "mix":
            await mix(client, query.message)

        elif query.data == "b|w":
            await black_white(client, query.message)
            
        elif query.data == "circlewithbg":
            await circle_with_bg(client, query.message)

        elif query.data == "circlewithoutbg":
            await circle_without_bg(client, query.message)

        elif query.data == "green":
            await green_border(client, query.message)

        elif query.data == "blue":
            await blue_border(client, query.message)

        elif query.data == "red":
            await red_border(client, query.message)

        elif query.data == "black":
            await black_border(client, query.message)

        elif query.data == "circle_sticker":
            await round_sticker(client, query.message)

        elif query.data == "inverted":
            await inverted(client, query.message)

        elif query.data == "stkr":
            await sticker(client, query.message)

        elif query.data == "cur_ved":
            await edge_curved(client, query.message)

        elif query.data == "90":
            await rotate_90(client, query.message)

        elif query.data == "180":
            await rotate_180(client, query.message)

        elif query.data == "270":
            await rotate_270(client, query.message)

        elif query.data == "contrast":
            await contrast(client, query.message)

        elif query.data == "box":
            await box_blur(client, query.message)

        elif query.data == "gas":
            await g_blur(client, query.message)

        elif query.data == "normal":
            await normal_blur(client, query.message)

        elif query.data == "sepia":
            await sepia_mode(client, query.message)

        elif query.data == "pencil":
            await pencil(client, query.message)

        elif query.data == "cartoon":
            await cartoon(client, query.message)

        elif query.data == "normalglitch1":
            await normalglitch_1(client, query.message)

        elif query.data == "normalglitch2":
            await normalglitch_2(client, query.message)

        elif query.data == "normalglitch3":
            await normalglitch_3(client, query.message)

        elif query.data == "normalglitch4":
            await normalglitch_4(client, query.message)

        elif query.data == "normalglitch5":
            await normalglitch_5(client, query.message)

        elif query.data == "scanlineglitch1":
            await scanlineglitch_1(client, query.message)

        elif query.data == "scanlineglitch2":
            await scanlineglitch_2(client, query.message)

        elif query.data == "scanlineglitch3":
            await scanlineglitch_3(client, query.message)

        elif query.data == "scanlineglitch4":
            await scanlineglitch_4(client, query.message)

        elif query.data == "scanlineglitch5":
            await scanlineglitch_5(client, query.message)

        elif query.data == "rmbgwhite":
            await removebg_white(client, query.message)

        elif query.data == "rmbgplain":
            await removebg_plain(client, query.message)

        elif query.data == "rmbgsticker":
            await removebg_sticker(client, query.message)
