from config import bot_token, forward_chat_id, admins_chat_id_list

import requests
from pprint import pprint
from time import sleep


sleep_time = 0.1

message_limit = 1
message_offset = 0


while(True):

    sleep(sleep_time)

    try:

        updates = requests.post(f'https://api.telegram.org/bot{bot_token}/getupdates?offset={message_offset}&limit={message_limit}')

        if len(updates.json()['result']) < 1:
            continue
        for message in updates.json()['result']:
            pprint(message)

        if 'message' in updates.json()['result'][0].keys():
            chat_id = updates.json()['result'][0]['message']['chat']['id']
            text = updates.json()['result'][0]['message']['text']


    except requests.exceptions.ConnectionError:
        print('connection error')
