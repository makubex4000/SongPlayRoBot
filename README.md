# Telegram SongPlayRoBot

Telegram bot for downloading audio from YouTube.

![logo](https://telegra.ph/file/9d337b3414bbf8e39ba79.jpg)

## Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/makubex2010/SongPlayRoBot)

## Manually

```
# Telegram API Key
# get from https://my.telegram.org/apps
export API_ID="1234567"
export API_HASH="0123456789abcdef0123456789abcdef"

# Telegram Bot Token
# get from https://t.me/BotFather
export BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"

# install ffmpeg
apt install ffmpeg

virtualenv venv
venv/bin/pip install -U -r requirements.txt
venv/bin/python SongPlayRoBot.py
```
