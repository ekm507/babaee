import subprocess
import special_commands
import requests
import json
from config import bot_token
import re

# this function clears ansi escape codes from text
def escape_ansi(line):
    # find all escape codes with regex
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    # clear them all
    return ansi_escape.sub('', line)
    
# process commands
def run_command(command, updates):

    # get chat id from message
    chat_id = updates.json()['result'][0]['message']['chat']['id']
    # text = updates.json()['result'][0]['message']['text']


    # try processing message and sending output
    try:
        # pick up first word of the message
        special_keyword = command.split(' ')[0]
        # if first word of message is one of the special commands:
        if special_keyword in special_commands.special_commands:
            # remove first word from the command text
            cmd = ' '.join(command.split(' ')[1:])
            # run special function for the command and get output
            out = special_commands.special_commands[special_keyword](cmd, chat_id)
        # if command is not one of the specials
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

    # if there was a permission error while running the command
    except PermissionError:
        # send proper Error message
        message = {
            "chat_id":chat_id,
            "text":'permissionError',
        }

    # if there was a file not found error while running the command
    except FileNotFoundError:
        # send proper error message
        message = {
            "chat_id":chat_id,
            "text":'FileNotFound',
        }

    # if there was any other error while running the command
    except subprocess.CalledProcessError as error_text:
        # send the error message got from command to telegram
        message = {
            "chat_id":chat_id,
            "text":f'ERROR: {error_text}',
        }

        # send the message
        requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data=message)
    # if there was any other Error
    except:
        # do not make a fuss!
        pass
