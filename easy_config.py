#!/usr/bin/python3

import requests
import random
from time import sleep
import os
import shutil

# read default config file
config_text = open('config.py.default').read()
config_file = open('config2.py', 'w')

files_in_dir = os.listdir()
if 'config.py' in files_in_dir:
    shutil.copyfile('config.py', 'config.py.bak')

print("create a bot using Botfather (https://t.me/BotFather)")
print("after creation you will get a token.")
bot_token = input("paste bot token here:")
config_text = config_text.replace('bot_token = ""', f'bot_token = "{bot_token}"')


password = str(random.randrange(1000, 9999))
print(f"now open chat of robot and send it this text: {password}")


# time to sleep between requests
sleep_time = 0.1

message_limit = 1
message_offset = 0



while(True):

    # this delay is for preventing high CPU load
    sleep(sleep_time)
    json_message = dict()

    # try getting messages and processing them
    try:

        # get message updates
        updates = requests.post(f'https://api.telegram.org/bot{bot_token}/getupdates?offset={message_offset}&limit={message_limit}')

        # pprint(updates.json())
        #  if there is no message, do nothing.
        if len(updates.json()['result']) < 1:
            # reloop it
            continue

        # print all new messages
        # for message in updates.json()['result']:
        #     pprint(message)

        # jsonified message to process
        json_message = updates.json()['result'][0]

        # type of message will be stored here. we will later use it for processing
        message_type = ''
        text = ''

        # if there is a new "message"
        if 'message' in json_message:


            # get chat id of the message
            chat_id = json_message['message']['chat']['id']
            message_id = json_message['message']['message_id']

            if 'text' in json_message['message']:

                # set message type
                message_type = 'text'
                # get message text
                # note: if message is not text type, error handling will catch it and continue the loop
                text = json_message['message']['text']


        # if there is not any key of the specified ones
        else:
            # mark message as read
            message_offset = json_message['update_id'] + 1
            # do nothing and just reloop it
            continue

        if message_type == 'text':
            if text == password:
                admins_chat_id = chat_id
                break
        # increase message offset. sending next request with this offset is like marking message as read.
        message_offset = json_message['update_id'] + 1
    
    except:
        pass
    


config_text = config_text.replace('admins_chat_id_list = [', f'admins_chat_id_list = [\n{admins_chat_id},')

# write config file
config_file.write(config_text)
config_file.close()
