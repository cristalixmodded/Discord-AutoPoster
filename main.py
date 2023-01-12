import json
import discum
import time
from datetime import datetime, timedelta
import random
import pytz

bot = discum.Client(token=input('Введите Ваш Discord-token: '))
channel_ID = input('Введите ID канала для отправки: ')
warp_name = input('Введите название рекламируемого Вами варпа: ')
MIN_delay = input('Введите минималый промежуток для отправки (в минутах): ')
MIN_delay = int(MIN_delay) * 60
MAX_delay = input('Введите максимальный промежуток для отправки (в минутах): ')
MAX_delay = int(MAX_delay) * 60 
advertisements = input('Введите рекламу (можно ввести несколько текстов через ; ): ')
advertisements = advertisements.split(';')

while True:
    last_message_id = None
    messages = bot.getMessages(channelID=channel_ID, num=100, beforeDate=last_message_id)
    messages = messages.text
    messages = messages.replace('\\n', '')
    messages = messages.replace('\\"', '')
    messages = messages.encode().decode("unicode-escape")
    messages = messages.replace('\\', '')

    messages = json.loads(messages)

    message_founded = False
    for j in messages:
        if not message_founded: 
            if j['author'].get('id') == '618536577282342912':
                content = j['content']
                if content.find(warp_name) != -1:
                    print(content.find(warp_name))
                    message_founded = True
                    message_timestamp = j['timestamp']
        last_message_id = j['id']

    if message_founded:
        message_founded = False
        last_message_id = None

        message_time = datetime.strptime(message_timestamp, '%Y-%m-%dT%H:%M:%S.%f+00:00')
        
        timezone = pytz.timezone('Europe/Moscow')
        time_now = datetime.now(timezone)
        time_now = time_now - timedelta(hours=3)
        time_now = time_now.replace(tzinfo=None)
        
        if message_time < time_now - timedelta(minutes=10):
            sended_message = bot.sendMessage(channelID=channel_ID, message=random.SystemRandom().choice(advertisements))
            sended_message = sended_message.text.encode().decode('unicode-escape')
            
            time.sleep(10)
            sended_message_json = json.loads(sended_message.replace('\\', ''))
            bot.deleteMessage(channelID=channel_ID, messageID=sended_message_json['id'])
            time.sleep(600)
        else:
            wait = message_time - time_now + timedelta(minutes=10)
            time.sleep(wait.total_seconds())
            time.sleep(random.randint(MIN_delay, MAX_delay))

    else:
        time.sleep(1)