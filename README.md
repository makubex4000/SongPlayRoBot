# Telegram 音樂機器人

用於 YouTube 的 Telegram 音樂機器人

。

## Heroku部屬

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/makubex2010/SongPlayRoBot)

## 手動部屬

```
# 電報 API 密鑰
# 從 https://my.telegram.org/apps 獲取
導出 API_ID="1234567"
導出 API_HASH="0123456789abcdef0123456789abcdef"

# 電報機器人令牌
# 從 https://t.me/BotFather 獲取
導出 BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"


# 安裝 ffmpeg
apt安裝ffmpeg

虛擬環境 venv
venv/bin/pip install -U -r requirements.txt
venv/bin/python tgmusicbot.py
```
