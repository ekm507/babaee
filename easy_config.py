#!/usr/bin/python3

import requests
import random

# read default config file
config_text = open('config.py.default').read()
config_file = open('config2.py', 'w')

# get token
print("create a bot using Botfather (https://t.me/BotFather)")
print("after creation you will get a token.")
bot_token = input("paste bot token here:")
config_text = config_text.replace('bot_token = ""', f'bot_token = "{bot_token}"')


password = str(random.randrange(1000, 9999))
print(f"now open chat of robot and send it this text: {password}")
admins_chat_id = 1234

config_text = config_text.replace('admins_chat_id_list = [', f'admins_chat_id_list = [\n{admins_chat_id},')

# write config file
config_file.write(config_text)
config_file.close()
