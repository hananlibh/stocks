from slack import WebClient
TOKEN = 'xoxb-1718477597872-1691553373925-sLmlcGaqhFZQ3o7RAIh3aTFl'
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
