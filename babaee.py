# import bot configurations
from config import bot_token, admins_chat_id_list
from run_command import run_command
import requests
from pprint import pprint
from time import sleep
import threading

# time to sleep between requests
sleep_time = 0.1

message_limit = 1
message_offset = 0

# main bot loop
while(True):

    # this delay is for preventing high CPU load
    sleep(sleep_time)

    # try getting messages and processing them
    try:

        # get message updates
        updates = requests.post(f'https://api.telegram.org/bot{bot_token}/getupdates?offset={message_offset}&limit={message_limit}')

        #  if there is no message, do nothing.
        if len(updates.json()['result']) < 1:
            # reloop it
            continue

        # print all new messages
        for message in updates.json()['result']:
            pprint(message)

        # if there is a new "message"
        if 'message' in updates.json()['result'][0].keys():
            # get chat id of the message
            chat_id = updates.json()['result'][0]['message']['chat']['id']
            # get message text
            # note: if message is not text type, error handling will catch it and continue the loop
            text = updates.json()['result'][0]['message']['text']

        # if there is a new "edited message"
        elif 'edited_message' in updates.json()['result'][0].keys():
            # get message chat_id
            chat_id = updates.json()['result'][0]['edited_message']['chat']['id']
            # get message text
            text = updates.json()['result'][0]['edited_message']['text']
        
        else:
            message_offset = updates.json()['result'][0]['update_id'] + 1
            continue

        # command is parsed only if message is sent from an admin
        if chat_id in admins_chat_id_list:
            # create a new thread for processing command
            x = threading.Thread(target=run_command, args=(text,updates))
            # start the thread
            x.start()


        # increase message offset. sending next request with this offset is like marking message as read.
        message_offset = updates.json()['result'][0]['update_id'] + 1
    
    # usually means message is in a type that is not supported in babaee (yet).
    except KeyError:
        # just mark message as read
        message_offset = updates.json()['result'][0]['update_id'] + 1

    # if there was a connection error
    except requests.exceptions.ConnectionError:
        # print error text but do not kill the bot.
        print('connection error')
