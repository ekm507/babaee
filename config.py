import os

# paste bot token here
bot_token = "" # "something:something"

# chat id of admins
admins_chat_id_list = [
     # integers
]

# a list of chat id. bot will forward all incoming messages to these users.
forward_chat_id_list = [
     # integers
]

# first path where program runs
main_path = os.path.realpath('.')

# direcroty for each user will be stored in this dictionary
# default dir is .
users_directories = {x:os.path.realpath('.') for x in admins_chat_id_list}
