# import bot configurations
from config import bot_token, admins_chat_id_list, forward_chat_id_list
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

        # pprint(updates.json())
        #  if there is no message, do nothing.
        if len(updates.json()['result']) < 1:
            # reloop it
            continue

        # print all new messages
        for message in updates.json()['result']:
            pprint(message)

        # jsonified message to process
        json_message = updates.json()['result'][0]

        # type of message will be stored here. we will later use it for processing
        message_type = ''

        # if there is a new "message"
        if 'message' in json_message.keys():

            # set message type
            message_type = 'message'

            # get chat id of the message
            chat_id = json_message['message']['chat']['id']
            # get message text
            # note: if message is not text type, error handling will catch it and continue the loop
            text = json_message['message']['text']

            # forward incomming message to specified chats.
            for forward_chat_id in forward_chat_id_list:

                # do not forward to themselves!
                if chat_id != int(forward_chat_id):

                    # forwarding message
                    forward_message = {
                        "chat_id":forward_chat_id,
                        "from_chat_id":json_message['message']['chat']['id'],
                        "message_id":json_message['message']['message_id'],
                    }

                    # send user identity
                    message = {
                        "chat_id":forward_chat_id,
                        "text": 'somebody(👇🏻) sent me a message(👆🏿)\n\n' + json_message['message']['chat'].__repr__(),
                    }

                    # forward message
                    requests.post(f'https://api.telegram.org/bot{bot_token}/forwardMessage', data=forward_message)
                    # send user identity
                    requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data=message)



        # if there is a new "edited message"
        elif 'edited_message' in json_message.keys():

            # set message type
            message_type = 'edited_message'

            # get message chat_id
            chat_id = json_message['edited_message']['chat']['id']
            # get message text
            text = json_message['edited_message']['text']


        # if message was actually a document
        elif 'document' in json_message:
            # set message type
            message_type = 'document'
            # get document info
            document_details = json_message['document']

        # if there is not any key of the specified ones
        else:
            # mark message as read
            message_offset = json_message['update_id'] + 1
            # do nothing and just reloop it
            continue


        # command is parsed only if message is sent from an admin
        if chat_id in admins_chat_id_list:
            # create a new thread for processing command
            x = threading.Thread(target=run_command, args=(text,updates))
            # start the thread
            x.start()


        # increase message offset. sending next request with this offset is like marking message as read.
        message_offset = json_message['update_id'] + 1
    
    # usually means message is in a type that is not supported in babaee (yet).
    except KeyError:
        # just mark message as read
        message_offset = json_message['update_id'] + 1

    # if there was a connection error
    except requests.exceptions.ConnectionError:
        # print error text but do not kill the bot.
        print('connection error')
