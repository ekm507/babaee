import subprocess
import special_commands
import requests
import json
from config import bot_token, users_directories, main_path, admins_chat_id_list, chatid_users, user_running_bot, reply_to_messages
import re
import os
import pickle
import re

# this function clears ansi escape codes from text
def escape_ansi(line):
    # find all escape codes with regex
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    # clear them all
    return ansi_escape.sub('', line)
    
# process commands
def run_command(command, chat_id, message_id):

    # text = updates.json()['result'][0]['message']['text']

    message = {}

    # change shell directory to users directory
    os.chdir(users_directories[chat_id])

    # try processing message and sending output
    try:
        # pick up first word of the message
        first_keyword = re.split(r' |\t|\n', command, 1)[0]
        # if first word of message is one of the special commands:
        if first_keyword in special_commands.special_commands:
            # remove first word from the command text
            cmd = re.split(r' |\t|\n', command, 1)[1]
            
            # run special function for the command and get output
            out = special_commands.special_commands[first_keyword](cmd, chat_id)

        # if command is not one of the specials
        else:

            if user_running_bot == 'root':
                
                username = chatid_users[chat_id]

                # run the command using subprocess and get output
                command_to_run = ['runuser' , username,'-c', command]
                out = subprocess.check_output(command_to_run)
            else:
                # run the command using subprocess and get output
                out = subprocess.check_output(command.split(' '))


        # remove ansi escape codes from command output
        # if out is str
        if isinstance(out, str):
            # just remove ansi escape characters
            printable_out_text = escape_ansi(out)
        # if it is not str 
        else:
            # first encode it into str, then remove ansi escape characters
            printable_out_text = escape_ansi(str(out, encoding='utf-8'))

        # make a message to send to telegram
        message = {
            # chat id should be id of the one who had requested
            "chat_id":chat_id,
            # text is command output in monospace format
            "text":'```\n' + printable_out_text + '\n```',
            # set parse mode to markdown so that text can be in monospace
            "parse_mode":"MarkdownV2",
        }
        if reply_to_messages == True:
            message.update({"reply_to_message_id":message_id,})

    # if there was a permission error while running the command
    except PermissionError:
        # send proper Error message
        message = {
            "chat_id":chat_id,
            "text":'permissionError',
        }
        if reply_to_messages == True:
            message.update({"reply_to_message_id":message_id,})


    # if there was a file not found error while running the command
    except FileNotFoundError:
        # send proper error message
        message = {
            "chat_id":chat_id,
            "text":'FileNotFound',
        }
        if reply_to_messages == True:
            message.update({"reply_to_message_id":message_id,})

    # if there was any other error while running the command
    except subprocess.CalledProcessError as error_text:
        # send the error message got from command to telegram
        message = {
            "chat_id":chat_id,
            "text":f'ERROR: {error_text}',
        }
        if reply_to_messages == True:
            message.update({"reply_to_message_id":message_id,})


    # if there was any other Error
    except:
        # do not make a fuss!
        pass

    # send the message
    requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data=message)


def check_document(document, chat_id, message_id):
    # make message to get more details from telegram
    message = {
        "file_id":document['file_id']
        }

    # ask telegram for file path of document
    responce = requests.post(f'https://api.telegram.org/bot{bot_token}/getFile', data=message)

    # get file path from responce
    file_path = responce.json()['result']['file_path']

    # get file name
    file_name = document['file_name']

    # change directory into robot dir
    os.chdir(main_path)
    # now we have to store (file_name, file_path, chat_id) somewhere.
    # we are going to make a dictionary and pickle.dump it

    try:
        users_file_paths = pickle.load(open('users_file_paths.pickle', 'rb'))
    except FileNotFoundError:
        users_file_paths = {id : ('', '') for id in admins_chat_id_list}
    
    users_file_paths[chat_id] = (file_name, file_path)
    
    pickle.dump(users_file_paths, open('users_file_paths.pickle', 'wb'))
    
    del users_file_paths

    # text message to send status to user
    message = {
        "chat_id":chat_id,
        "text":'OK! I see your file.\nif you want to store it, send /receive command.',
    }
    if reply_to_messages == True:
        message.update({"reply_to_message_id":message_id,})

    # tell user that file is seen
    requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data=message)
