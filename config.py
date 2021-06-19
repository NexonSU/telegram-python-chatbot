#!/usr/bin/env python

#loglevel: CRITICAL - 50, ERROR - 40, WARNING - 30, INFO - 20, DEBUG - 10
loglevel = 30
logformat = "%(asctime)s - %(levelname)s - %(message)s"
logdatefmt = "%d.%m.%Y %H:%M:%S"

#telegram
telegram_token = '' #to get token, create bot via @botfather at telegram https://t.me/BotFather
telegram_chat = '@' #your telegram chatgroup
telegram_stream_channel = '@' #your telegram stream channel
telegram_channel = '@' #your telegram channel
telegram_bot_api_url = 'https://api.telegram.org/bot' #your telegram bot api server. Official server: https://api.telegram.org/bot
telegram_admins = [] #telegram chatgroup admins
telegram_moders = [] #telegram chatgroup moders
telegram_sysadmin =  #your ID

#telegram webhook
telegram_webhook_listen = "127.0.0.1"
telegram_webhook_port = 8440
telegram_webhook_allowed_updates = ['message', 'channel_post', 'callback_query', 'chat_member']

#youtube
youtube_apikey = '' #to get token, go to https://console.cloud.google.com/apis/credentials
youtube_channelname = '' #telegram channel without @
youtube_channelid = '' #your youtube channel ID. To get channel ID, just open "Your channel" from user panel dock and copy channel ID from address bar.

#extras
currency_apikey = '' #https://pro.coinmarketcap.com/
ics_url = '' #game releases calendar in ics format