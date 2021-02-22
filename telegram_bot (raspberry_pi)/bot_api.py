import requests

bot_token = 'YOUR_BOT_TOKEN'
chat_id = '388305285' # Kians
url = f'https://api.telegram.org/bot{bot_token}'

def send_text(bot_message):
    response = requests.get(f'{url}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={bot_message}')
    return response.json()


def send_image(imageFile):
    response = requests.post(f'{url}/sendPhoto', data={'chat_id': chat_id}, files={'photo': open(imageFile, 'rb')})
    return response.json()
