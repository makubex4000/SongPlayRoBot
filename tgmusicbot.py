"""

tgmusicbot，電報音頻下載機器人
版權所有 (C) 2021 Dash Eclipse

該程序是免費軟件：您可以重新分發和/或修改
它根據 GNU Affero 通用公共許可證的條款，由
自由軟件基金會，許可證的第 3 版，或
（由您選擇）任何更高版本。

這個程序是分發的，希望它有用，
但沒有任何保證； 甚至沒有暗示的保證
特定用途的適銷性或適用性。 見
有關更多詳細信息，請參閱 GNU Affero 通用公共許可證。

您應該已經收到一份 GNU Affero 通用公共許可證的副本
隨著這個程序。 如果沒有，請參閱 <https://www.gnu.org/licenses/>。


從 YouTube/SoundCloud/Mixcloud 下載音樂，轉換縮略圖
方形縮略圖並上傳到電報

發送鏈接作為繞過音樂類別檢查的回覆

# requirements.txt
OpenCC
Pillow
youtube-dl

# ../../config.py
MUSIC_CHATS = [
    -1234567891012,
    -2345678910123
]
MUSIC_USERS = [1234567890]
MUSIC_DELAY_DELETE_INFORM = 10
MUSIC_INFORM_AVAILABILITY = (
    "此機器人僅服務於指定的群組和"
    "其成員在私人聊天"
)
MUSIC_MAX_LENGTH = 10800

"""
import os
import asyncio
from datetime import timedelta
from urllib.parse import urlparse
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from yt_dlp import YoutubeDL
from PIL import Image
import ffmpeg

MUSIC_MAX_LENGTH = 10800
DELAY_DELETE_INFORM = 10
TG_THUMB_MAX_LENGTH = 320
REGEX_SITES = (
    r"^((?:https?:)?\/\/)"
    r"?((?:www|m)\.)"
    r"?((?:youtube\.com|youtu\.be|soundcloud\.com|mixcloud\.com))"
    r"(\/)([-a-zA-Z0-9()@:%_\+.~#?&//=]*)([\w\-]+)(\S+)?$"
)
REGEX_EXCLUDE_URL = (
    r"\/channel\/|\/playlist\?list=|&list=|\/sets\/"
)


def get_music_chats():
    chats = []
    for x in os.environ["MUSIC_CHATS"].split(" "):
        try:
            chats.append(int(x))
        except ValueError:
            chats.append(x)
    return chats


MUSIC_CHATS = get_music_chats()
API_ID = os.environ["API_ID"]
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
app = Client(
    "tgmusicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# - handlers and functions
main_filter = (
    filters.text
    & filters.chat(MUSIC_CHATS)
    & filters.incoming
    & ~filters.edited
)


@app.on_message(main_filter & filters.regex("^/ping$"))
async def ping_pong(_, message):
    await _reply_and_delete_later(message, "pong",
                                  DELAY_DELETE_INFORM)


@app.on_message(main_filter
                & filters.regex(REGEX_SITES)
                & ~filters.regex(REGEX_EXCLUDE_URL))
async def music_downloader(_, message: Message):
    await _fetch_and_send_music(message)


async def _fetch_and_send_music(message: Message):
    await message.reply_chat_action("typing")
    try:
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': '%(title)s - %(extractor)s-%(id)s.%(ext)s',
            'writethumbnail': True
        }
        ydl = YoutubeDL(ydl_opts)
        info_dict = ydl.extract_info(message.text, download=True)
        # send a link as a reply to bypass Music category check
        if not message.reply_to_message \
                and _youtube_video_not_music(info_dict):
            inform = ("此影片不屬於音樂類別， "
                      "您可以在您發送的連結"
                      "回覆剛剛的連結"
                      "強制下載")
            await _reply_and_delete_later(message, inform,
                                          DELAY_DELETE_INFORM)
            return
        if info_dict['duration'] > MUSIC_MAX_LENGTH:
            readable_max_length = str(timedelta(seconds=MUSIC_MAX_LENGTH))
            inform = ("音頻長度超過機器人設置的長度"
                      .format(readable_max_length))
            await _reply_and_delete_later(message, inform,
                                          DELAY_DELETE_INFORM)
            return
        d_status = await message.reply_text("下載中，請稍後...", quote=True,
                                            disable_notification=True)
        ydl.process_info(info_dict)
        audio_file = ydl.prepare_filename(info_dict)
        task = asyncio.create_task(_upload_audio(message, info_dict,
                                                 audio_file))
        await message.reply_chat_action("upload_document")
        await d_status.delete()
        while not task.done():
            await asyncio.sleep(4)
            await message.reply_chat_action("upload_document")
        await message.reply_chat_action("cancel")
        if message.chat.type == "private":
            await message.delete()
    except Exception as e:
        await message.reply_text(repr(e))


def _youtube_video_not_music(info_dict):
    if info_dict['extractor'] == 'youtube' \
            and 'Music' not in info_dict['categories']:
        return True
    return False


async def _reply_and_delete_later(message: Message, text: str, delay: int):
    reply = await message.reply_text(text, quote=True)
    await asyncio.sleep(delay)
    await reply.delete()


async def _upload_audio(message: Message, info_dict, audio_file):
    basename = audio_file.rsplit(".", 1)[-2]
    if info_dict['ext'] == 'webm':
        audio_file_opus = basename + ".opus"
        ffmpeg.input(audio_file).output(audio_file_opus, codec="copy").run()
        os.remove(audio_file)
        audio_file = audio_file_opus
    thumbnail_url = info_dict['thumbnail']
    if os.path.isfile(basename + ".jpg"):
        thumbnail_file = basename + ".jpg"
    else:
        thumbnail_file = basename + "." + \
            _get_file_extension_from_url(thumbnail_url)
    squarethumb_file = basename + "_squarethumb.jpg"
    make_squarethumb(thumbnail_file, squarethumb_file)
    webpage_url = info_dict['webpage_url']
    title = info_dict['title']
    caption = f"<b><a href=\"{webpage_url}\">{title}</a></b>"
    duration = int(float(info_dict['duration']))
    performer = info_dict['uploader']
    await message.reply_audio(audio_file,
                              caption=caption,
                              duration=duration,
                              performer=performer,
                              title=title,
                              parse_mode='HTML',
                              thumb=squarethumb_file)
    for f in (audio_file, thumbnail_file, squarethumb_file):
        os.remove(f)


def _get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]


def make_squarethumb(thumbnail, output):
    """Convert thumbnail to square thumbnail"""
    # https://stackoverflow.com/a/52177551
    original_thumb = Image.open(thumbnail)
    squarethumb = _crop_to_square(original_thumb)
    squarethumb.thumbnail((TG_THUMB_MAX_LENGTH, TG_THUMB_MAX_LENGTH),
                          Image.ANTIALIAS)
    squarethumb.save(output)


def _crop_to_square(img):
    width, height = img.size
    length = min(width, height)
    left = (width - length) / 2
    top = (height - length) / 2
    right = (width + length) / 2
    bottom = (height + length) / 2
    return img.crop((left, top, right, bottom))


# - start


app.start()
print('>>> BOT STARTED')
idle()
app.stop()
print('\n>>> BOT STOPPED')
