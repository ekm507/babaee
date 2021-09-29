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



if user_running_bot == 'root':

     # each chat id is assigned to a user in linux.
     # this is a dictionary.
     # each element is like this:
     # chat_id:'username'
     # for example:
     # 12121212:'root',
     chatid_users = {
          # integer:string
     }
else:
     chatid_users = {chat_id:user_running_bot for chat_id in admins_chat_id_list}

sudoers_chatid = [
     #integer
]