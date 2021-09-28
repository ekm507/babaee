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

# file containing a help for robot
# change it to any help file you would like to be sent to user when using /help command.
help_file_name = 'README.md'

# start message for bot. this message will be sent to forward 
bot_start_message = 'bot started working! 🐑'
