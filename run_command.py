import subprocess
import requests
import json
from config import bot_token


def run_command(command, updates):

    chat_id = updates.json()['result'][0]['message']['chat']['id']
    # text = updates.json()['result'][0]['message']['text']



    try:
        out = subprocess.check_output(command.split(' '))

        message = {
            "chat_id":chat_id,
            "text":'```\n' + str(out, encoding='utf-8') + '\n```',
            "parse_mode":"MarkdownV2",
        }


    except PermissionError:
        message = {
            "chat_id":chat_id,
            "text":'permissionError',
        }

    except FileNotFoundError:
        message = {
            "chat_id":chat_id,
            "text":'FileNotFound',
        }

    except subprocess.CalledProcessError as error_text:
        message = {
            "chat_id":chat_id,
            "text":f'ERROR: {error_text}',
        }

        requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data=message)
    except:
        pass
