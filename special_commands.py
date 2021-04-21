import subprocess
import requests
from config import bot_token

# run command using sh shell
def __run_sh__(command : str, chat_id):
    # run command using sh shell
    return subprocess.check_output(command, shell=True)

# print a text into a file
def __edit_file__(command : str, chat_id):
    # get filename. first word in the message should be the filename
    fileName = command.split(' ')[0].split('\n')[0]
    # if we remove first work from the message, remaining will be text body of file
    text = command[len(fileName)+1:]

    # if text is empty, do nothing. (there is some reason for now)
    if len(text) < 1:
        pass

    # try to open a file and write text into
    try:
        # open the file
        with open(fileName, 'w') as fileToEdit:
            # write text into file
            fileToEdit.write(text)
        # return a proper success message.
        return 'File edited successfully'
    # if there was any error opening or writing into file
    except:
        # return suitable error message
        return 'Error: there was an error editing file'


# send a file to telegram chat
def __send_file__(command:str, chat_id):

    # get filename
    filename = command

    # data part of request
    message = {
        "chat_id":chat_id,
    }

    # file part of request
    files = {
        # open file and put it in files part of request
        "document":open(filename, 'rb'),
    }

    # send file into telegram
    requests.post(f'https://api.telegram.org/bot{bot_token}/sendDocument', data=message, files=files)
    return ''

# send a message worth of robot help
def __print_help_message__(command, chat_id):

    with open('robotHelp.markdownV2') as help_file:
        help_text = help_file.read()

    message = {
        "chat_id":chat_id,
        # "parse_mode":"MarkdownV2",
        "text":help_text,
    }

    requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data=message)
    return ''


# todo. this is just a temporary solution!!!
def __show_process_list__(command, chat_id):
    text = subprocess.check_output('ps')
    return text


# a dict of special commands mapped to corresponding function
special_commands = {
    '/sh':__run_sh__,
    '/edit':__edit_file__,
    '/send':__send_file__,
    '/help': __print_help_message__,
    '/ps': __show_process_list__,

}

