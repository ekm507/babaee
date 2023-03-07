#!/usr/bin/python3

import requests

# read default config file
config_text = open('config.py.default').read()
config_file = open('config2.py', 'w')

# get token
bot_token = input("paste bot token here:")
config_text = config_text.replace('bot_token = ""', f'bot_token = "{bot_token}"')


admins_chat_id = 1234

config_text = config_text.replace('admins_chat_id_list = [', f'admins_chat_id_list = [\n{admins_chat_id},')

# write config file
config_file.write(config_text)
config_file.close()
