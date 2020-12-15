
import datetime
import html
import textwrap
import bs4
import jikanpy
import requests
from telegraph import Telegraph
from inspect import getfullargspec

from pyrogram import Client, filters
from pyrogram.types import Message, Update, InlineKeyboardMarkup, InlineKeyboardButton

from SaitamaRobot import pbot

telegraph = Telegraph()
telegraph.create_account(short_name='hitsuki')
info_btn = "More Information"
url = 'https://graphql.anilist.co'


airing_query = '''
    query ($id: Int,$search: String) {
      Media (id: $id, type: ANIME,search: $search) {
        id
        episodes
        title {
          romaji
          english
          native
        }
        siteUrl
        nextAiringEpisode {
           airingAt
           timeUntilAiring
           episode
        }
      }
    }
'''

fav_query = """
query ($id: Int) {
      Media (id: $id, type: ANIME) {
        id
        title {
          romaji
          english
          native
        }
     }
}
"""

anime_query = '''
   query ($id: Int,$search: String) {
      Media (id: $id, type: ANIME,search: $search) {
        id
        idMal
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          season
          type
          format
          status
          duration
          siteUrl
          studios{
              nodes{
                   name
              }
          }
          trailer{
               id
               site
               thumbnail
          }
          averageScore
          genres
          bannerImage
      }
    }
'''

character_query = """
    query ($query: String) {
        Character (search: $query) {
               id
               name {
                     first
                     last
                     full
               }
               siteUrl
               favourites
               image {
                        large
               }
               description
        }
    }
"""

manga_query = """
query ($id: Int,$search: String) {
      Media (id: $id, type: MANGA,search: $search) {
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          type
          format
          status
          siteUrl
          averageScore
          genres
          bannerImage
      }
    }
"""


def shorten(description, info='anilist.co'):
    ms_g = ""
    if len(description) > 700:
        description = description[0:500] + '...'
        ms_g += f"\n**Description**: __{description}__ [Read More]({info})"
    else:
        ms_g += f"\n**Description**: __{description}__"
    return (
        ms_g.replace("<br>", "")
        .replace("</br>", "")
        .replace("<i>", "")
        .replace("</i>", "")
    )


# time formatter from uniborg
def t(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " Days, ") if days else "") + \
        ((str(hours) + " Hours, ") if hours else "") + \
        ((str(minutes) + " Minutes, ") if minutes else "") + \
        ((str(seconds) + " Seconds, ") if seconds else "") + \
        ((str(milliseconds) + " ms, ") if milliseconds else "")
    return tmp[:-2]


async def edrep(m: Message, **kwargs):
    func = m.edit_text if m.from_user.is_self else m.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


@pbot.on_message(filters.command('airing'))
async def anime_airing(c: Client, m: Message):
    search_str = m.text.split(' ', 1)
    chat_id = m.chat.id
    if len(search_str) == 1:
        await m.reply_text(tld(chat_id, "anime_no_arg"))
        return
    variables = {'search': search_str[1]}
    response = requests.post(
        url, json={'query': airing_query, 'variables': variables}).json()['data']['Media']
    ms_g = f"**Name**: **{response['title']['romaji']}**(`{response['title']['native']}`)\n**ID**: `{response['id']}`"
    if response['nextAiringEpisode']:
        airing_time = response['nextAiringEpisode']['timeUntilAiring'] * 1000
        airing_time_final = t(airing_time)
        ms_g += f"\n**Episode**: `{response['nextAiringEpisode']['episode']}`\n**Airing In**: `{airing_time_final}`"
    else:
        ms_g += f"\n**Episode**: `{response['episodes']}`\n**Status**: `N/A`"
    await m.reply_text(ms_g)


@pbot.on_message(filters.command('anime'))
async def anime_search(c: Client, m: Message):
    search = m.text.split(' ', 1)
    chat_id = m.chat.id
    if len(search) == 1:
        await m.reply_text(tld(chat_id, "anime_no_arg"))
        return
    else:
        search = search[1]
    variables = {'search': search}
    json = requests.post(url, json={'query': anime_query, 'variables': variables}).json()[
        'data'].get('Media', None)
    if json:
        msg = f"**{json['title']['romaji']}**(`{json['title']['native']}`)\n**Type**: {json['format']}\n**Status**: {json['status']}\n**Episodes**: {json.get('episodes', 'N/A')}\n**Duration**: {json.get('duration', 'N/A')} Per Ep.\n**Score**: {json['averageScore']}\n**Genres**: `"
        for x in json['genres']:
            msg += f"{x}, "
        msg = msg[:-2] + '`\n'
        msg += tld(chat_id, "anime_studios")
        for x in json['studios']['nodes']:
            msg += f"{x['name']}, "
        msg = msg[:-2] + '`\n'
        info = json.get('siteUrl')
        trailer = json.get('trailer', None)
        if trailer:
            trailer_id = trailer.get('id', None)
            site = trailer.get('site', None)
            if site == "youtube":
                trailer = 'https://youtu.be/' + trailer_id
        description = json.get(
            'description', 'N/A').replace('<i>', '').replace('</i>', '').replace('<br>', '')
        msg += shorten(description, info)
        image = info.replace('anilist.co/anime/', 'img.anili.st/media/')
        more_info = tld(chat_id, "anime_more_info")
        if trailer:
            buttons = [
                [InlineKeyboardButton(more_info, url=info),
                 InlineKeyboardButton("Trailer 🎬", url=trailer)]
            ]
        else:
            buttons = [
                [InlineKeyboardButton(more_info, url=info)]
            ]
        if image:
            try:
                await m.reply_photo(image, caption=msg, reply_markup=InlineKeyboardMarkup(buttons))
            except Exception:
                msg += f" [〽️]({image})"
                await m.edit(msg)
        else:
            await m.edit(msg)


@pbot.on_message(filters.command('character'))
async def character_search(c: Client, m: Message):
    search = m.text.split(' ', 1)
    chat_id = m.chat.id
    if len(search) == 1:
        await m.reply_text(tld(chat_id, "character_no_arg"))
        return
    search = search[1]
    variables = {'query': search}
    json = requests.post(url, json={'query': character_query, 'variables': variables}).json()[
        'data'].get('Character', None)
    if json:
        ms_g = f"**{json.get('name').get('full')}**(`{json.get('name').get('native')}`)\n"
        description = f"{json['description']}"
        site_url = json.get('siteUrl')
        ms_g += shorten(description, site_url)
        image = json.get('image', None)
        if image:
            image = image.get('large')
            await m.reply_photo(image, caption=ms_g)
        else:
            await edrep(m, text=ms_g)


@pbot.on_message(filters.command('manga'))
async def manga_search(c: Client, m: Message):
    search = m.text.split(' ', 1)
    chat_id = m.chat.id
    if len(search) == 1:
        await m.reply_text(tld(chat_id, "manga_no_arg"))
        return
    search = search[1]
    variables = {'search': search}
    json = requests.post(url, json={'query': manga_query, 'variables': variables}).json()[
        'data'].get('Media', None)
    ms_g = ''
    if json:
        title, title_native = json['title'].get(
            'romaji', False), json['title'].get('native', False)
        start_date, status, score = json['startDate'].get('year', False), json.get(
            'status', False), json.get('averageScore', False)
        if title:
            ms_g += f"**{title}**"
            if title_native:
                ms_g += f"(`{title_native}`)"
        if start_date:
            ms_g += tld(chat_id, "manga_start_date").format(start_date)
        if status:
            ms_g += tld(chat_id, "manga_status").format(status)
        if score:
            ms_g += tld(chat_id, "manga_score").format(score)
        ms_g += tld(chat_id, "manga_genre")
        for x in json.get('genres', []):
            ms_g += f"{x}, "
        ms_g = ms_g[:-2]

        image = json.get("bannerImage", False)
        ms_g += f"\n__{json.get('description', None)}__"
        if image:
            try:
                await m.reply_photo(image, caption=ms_g)
            except Exception:
                ms_g += f" [〽️]({image})"
                await edrep(m, text=ms_g)
        else:
            await edrep(m, text=ms_g)


@pbot.on_message(filters.command('user'))
async def user(c: Client, m: Message):
    args = m.text.split(' ', 1)

    try:
        search_query = args[1]
    except BaseException:
        if m.reply_to_message:
            search_query = m.reply_to_message.text
        else:
            await m.reply_text("Format: /user <username>")
            return

    jikan = jikanpy.jikan.Jikan()

    try:
        user = jikan.user(search_query)
    except jikanpy.APIException:
        await m.reply_text("Username not found.")
        return

    progress_message = await m.reply_text("Searching...")

    date_format = "%Y-%m-%d"
    if user['image_url'] is None:
        img = "https://cdn.myanimelist.net/images/questionmark_50.gif"
    else:
        img = user['image_url']

    try:
        user_birthday = datetime.datetime.fromisoformat(user['birthday'])
        user_birthday_formatted = user_birthday.strftime(date_format)
    except BaseException:
        user_birthday_formatted = "Unknown"

    user_joined_date = datetime.datetime.fromisoformat(user['joined'])
    user_joined_date_formatted = user_joined_date.strftime(date_format)

    for entity in user:
        if user[entity] is None:
            user[entity] = "Unknown"

    caption = ""

    caption += textwrap.dedent(f"""
    **Username**: [{user['username']}]({user['url']})

    **Gender**: `{user['gender']}`
    **Birthday**: `{user_birthday_formatted}`
    **Joined**: `{user_joined_date_formatted}`
    **Days wasted watching anime**: `{user['anime_stats']['days_watched']}`
    **Days wasted reading manga**: `{user['manga_stats']['days_read']}`

    """)

    buttons = [[InlineKeyboardButton(info_btn, url=user['url'])]]

    await m.reply_photo(
        photo=img,
        caption=caption,
        parse_mode="markdown",
        reply_markup=InlineKeyboardMarkup(buttons))
    await progress_message.delete()


@pbot.on_message(filters.command('upcoming'))
async def upcoming(c: Client, m: Message):
    jikan = jikanpy.jikan.Jikan()
    upcoming = jikan.top('anime', page=1, subtype="upcoming")

    upcoming_list = [entry['title'] for entry in upcoming['top']]
    upcoming_message = ""

    for entry_num in range(len(upcoming_list)):
        if entry_num == 10:
            break
        upcoming_message += f"{entry_num + 1}. {upcoming_list[entry_num]}\n"

    await m.reply_text(upcoming_message)


@pbot.on_message(filters.command('nhentai'))
async def nhentai(c: Client, m: Message):
    query = m.text.split(" ")[1]
    title, tags, artist, total_pages, post_url, cover_image = nhentai_data(
        query)
    await m.reply_text(
        f"<code>{title}</code>\n\n<b>Tags:</b>\n{tags}\n<b>Artists:</b>\n{artist}\n<b>Pages:</b>\n{total_pages}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Read Here",
                        url=post_url
                    )
                ]
            ]
        )
    )


def nhentai_data(noombers):
    url = f"https://nhentai.net/api/gallery/{noombers}"
    res = requests.get(url).json()
    pages = res["images"]["pages"]
    info = res["tags"]
    title = res["title"]["english"]
    links = []
    tags = ""
    artist = ''
    total_pages = res['num_pages']
    post_content = ""

    extensions = {
        'j': 'jpg',
        'p': 'png',
        'g': 'gif'
    }
    for i, x in enumerate(pages):
        media_id = res["media_id"]
        temp = x['t']
        file = f"{i+1}.{extensions[temp]}"
        link = f"https://i.nhentai.net/galleries/{media_id}/{file}"
        links.append(link)

    for i in info:
        if i["type"] == "tag":
            tag = i['name']
            tag = tag.split(" ")
            tag = "_".join(tag)
            tags += f"#{tag} "
        if i["type"] == "artist":
            artist = f"{i['name']} "

    for link in links:
        post_content += f"<img src={link}><br>"

    post = telegraph.create_page(
        f"{title}",
        html_content=post_content,
        author_name="Hitsuki",
        author_url="https://t.me/LordHitsuki_BOT"
    )
    return title, tags, artist, total_pages, post['url'], links[0]


async def site_search(client: Client, m: Message, site: str):
    args = m.text.split(' ', 1)
    more_results = True

    try:
        search_query = args[1]
    except IndexError:
        await m.reply_text("Give something to search")
        return

    if site == "kaizoku":
        search_url = f"https://animekaizoku.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {'class': "post-title"})

        if search_result:
            result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>: \n"
            for entry in search_result:
                post_link = entry.a['href']
                post_name = html.escape(entry.text)
                result += f"• <a href='{post_link}'>{post_name}</a>\n"
        else:
            more_results = False
            result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>"

    elif site == "kayo":
        search_url = f"https://animekayo.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {'class': "title"})

        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>: \n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>"
                more_results = False
                break

            post_link = entry.a['href']
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"

    buttons = [[InlineKeyboardButton("See all results", url=search_url)]]

    if more_results:
        await m.reply_text(
            result,
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True)
    else:
        await m.reply_text(
            result, parse_mode="html", disable_web_page_preview=True)


@pbot.on_message(filters.command('kaizoku'))
async def kaizoku(c: Client, update: Update):
    await site_search(c, update, "kaizoku")


@pbot.on_message(filters.command('kayo'))
async def kayo(c: Client, update: Update):
    await site_search(c, update, "kayo")


__help__ = True
