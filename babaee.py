from config import bot_token, admins_chat_id_list

import requests
from pprint import pprint
from time import sleep
import threading
from run_command import run_command

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

        elif 'edited_message' in updates.json()['result'][0].keys():
            chat_id = updates.json()['result'][0]['edited_message']['chat']['id']
            text = updates.json()['result'][0]['edited_message']['text']

        print('\n')


        if chat_id in admins_chat_id_list:
            x = threading.Thread(target=run_command, args=(text,updates))
            x.start()


        message_offset = updates.json()['result'][0]['update_id'] + 1
    
    # usually means message is in a type that is not supported in babaee (yet).
    except KeyError:
        message_offset = updates.json()['result'][0]['update_id'] + 1

    except requests.exceptions.ConnectionError:
        print('connection error')
