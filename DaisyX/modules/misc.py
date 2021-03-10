from contextlib import suppress

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from aiogram.types import Message
from aiogram.utils.exceptions import BadRequest, MessageNotModified, MessageToDeleteNotFound

from DaisyX.decorator import register
from .utils.language import get_strings_dec
from .utils.notes import get_parsed_note_list, send_note, t_unparse_note_item
from .utils.user_details import is_user_admin


@register(cmds='cancel', state='*', allow_kwargs=True)
async def cancel_handle(message, state, **kwargs):
    await state.finish()
    await message.reply('Cancelled.')


async def delmsg_filter_handle(message, chat, data):
    if await is_user_admin(data['chat_id'], message.from_user.id):
        return
    with suppress(MessageToDeleteNotFound):
        await message.delete()


async def replymsg_filter_handler(message, chat, data):
    text, kwargs = await t_unparse_note_item(message, data['reply_text'], chat['chat_id'])
    kwargs['reply_to'] = message.message_id
    with suppress(BadRequest):
        await send_note(chat['chat_id'], text, **kwargs)


@get_strings_dec('misc')
async def replymsg_setup_start(message, strings):
    with suppress(MessageNotModified):
        await message.edit_text(strings['send_text'])


async def replymsg_setup_finish(message, data):
    reply_text = await get_parsed_note_list(message, allow_reply_message=False, split_args=-1)
    return {'reply_text': reply_text}


@get_strings_dec('misc')
async def customise_reason_start(message: Message, strings: dict):
    await message.reply(strings['send_customised_reason'])


@get_strings_dec('misc')
async def customise_reason_finish(message: Message, _: dict, strings: dict):
    if message.text is None:
        await message.reply(strings['expected_text'])
        return False
    elif message.text in {'None'}:
        return {'reason': None}
    return {'reason': message.text}


__filters__ = {
    'delete_message': {
        'title': {'module': 'misc', 'string': 'delmsg_filter_title'},
        'handle': delmsg_filter_handle,
        'del_btn_name': lambda msg, data: f"Del message: {data['handler']}"
    },
    'reply_message': {
        'title': {'module': 'misc', 'string': 'replymsg_filter_title'},
        'handle': replymsg_filter_handler,
        'setup': {
            'start': replymsg_setup_start,
            'finish': replymsg_setup_finish
        },
        'del_btn_name': lambda msg, data: f"Reply to {data['handler']}: \"{data['reply_text'].get('text', 'None')}\" "
    }
}


@register(cmds='buttonshelp', no_args=True, only_pm=True)
async def buttons_help(message):
    await message.reply(
        """
<b>Buttons:</b>
Here you will know how to setup buttons in your note, welcome note, etc...

There are different types of buttons!

<i>Due to current Implementation adding invalid button syntax to your note will raise error! This will be fixed in next major version.</i>

<b>Did you know?</b>
You could save buttons in same row using this syntax
<code>[Button](btn{mode}:{args if any}:same)</code>
(adding <code>:same</code> like that does the job.)

<b>Button Note:</b>
<i>Don't confuse this title with notes with buttons</i> 😜

This types of button will allow you to show specific notes to users when they click on buttons!

You can save note with button note without any hassle by adding below line to your note ( Don't forget to replace <code>notename</code> according to you 😀)

<code>[Button Name](btnnote:notename)</code>

<b>URL Button:</b>
Ah as you guessed! This method is used to add URL button to your note. With this you can redirect users to your website or even redirecting them to any channel, chat or messages!

You can add URL button by adding following syntax to your note

<code>[Button Name](btnurl:https://your.link.here)</code>

<b>Button rules:</b>
Well in v2 we introduced some changes, rules are now saved seperately unlike saved as note before v2 so it require seperate button method!

You can use this button method for including Rules button in your welcome messages, filters etc.. literally anywhere*

You use this button with adding following syntax to your message which support formatting!
<code>[Button Name](btnrules)</code>
    """
    )


@register(cmds='variableshelp', no_args=True, only_pm=True)
async def buttons_help(message):
    await message.reply(
        """
<b>Variables:</b>
Variables are special words which will be replaced by actual info

<b>Avaible variables:</b>
<code>{first}</code>: User's first name
<code>{last}</code>: User's last name
<code>{fullname}</code>: User's full name
<code>{id}</code>: User's ID
<code>{mention}</code>: Mention the user using first name
<code>{username}</code>: Get the username, if user don't have username will be returned mention
<code>{chatid}</code>: Chat's ID
<code>{chatname}</code>: Chat name
<code>{chatnick}</code>: Chat username
    """
    )


__mod_name__ = "Misc"

__help__ = """
An "odds and ends" module for small, simple commands which don't really fit anywhere.

<b>Available commands:</b>
- /cancel: Disables current state. Can help in cases if AllMight not responing on your message.
- /id: get the current group id. If used by replying to a message, gets that user's id.
- /info: get information about a user.
"""
