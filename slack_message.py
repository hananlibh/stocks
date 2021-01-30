import json
from slack import WebClient

with open('config.json') as config_file:
    config = json.load(config_file)

TOKEN = config['REDDIT_BOT_TOKEN']
WALLSTREETBETS_CHANNEL = 'wallstreetbets'


def send_notification(message=''):
    client = WebClient(TOKEN)
    client.chat_postMessage(channel=WALLSTREETBETS_CHANNEL,
                            text="<#{}> {}!".format(WALLSTREETBETS_CHANNEL, message))


def send_file(file_path=''):
    client = WebClient(TOKEN)
    client.files_upload(channels=WALLSTREETBETS_CHANNEL,
                        file=file_path,
                        text="Hourly file upload")
