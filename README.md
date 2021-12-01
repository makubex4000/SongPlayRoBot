# Telegram 音樂機器人

用於 YouTube/SoundCloud/Mixcloud 的 Telegram 音樂機器人

當有人發送 YouTube/SoundCloud/MixCloud 連結時，此機器人會下載並發送音頻
在指定的聊天中，有一個命令 `/ping` 使機器人回复“ping”
用於檢查機器人是否正在運行。

## Heroku部屬

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/makubex2010/Telegram-music-bot)

## 手動部屬

```
# 電報 API 密鑰
# 從 https://my.telegram.org/apps 獲取
導出 API_ID="1234567"
導出 API_HASH="0123456789abcdef0123456789abcdef"

# 電報機器人令牌
# 從 https://t.me/BotFather 獲取
導出 BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"

# 機器人服務的一個或多個用戶/組用戶名/ID，
# 用空格隔開
導出 MUSIC_CHATS="-100123456789 用戶名"

# 安裝 ffmpeg
apt安裝ffmpeg

虛擬環境 venv
venv/bin/pip install -U -r requirements.txt
venv/bin/python tgmusicbot.py
```
