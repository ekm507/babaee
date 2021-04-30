import subprocess
import requests
from config import bot_token

# run command using sh shell
def __run_sh__(command : str, chat_id):
    # run command using sh shell
    return subprocess.check_output(command, shell=True)

# print a text into a file
def __edit_file__(command : str, chat_id):

    # first line of command is args line
    args = list(filter(('').__ne__, command.split('\n')[0].split(' ')))

    # if there is a -a switch in args, it means that file should be appended.
    if '-a' in args:
        write_mode = 'a'
    else:
        write_mode = 'w'
    
    # get filename. first word in the message should be the filename
    for arg in args:
        if arg not in ['-a']:
            fileName = arg
            break

    # if we remove first line from the message, remaining will be text body of file
    text = command[len(command.split('\n')[0])+1:]

    # if text is empty, do nothing. (there is some reason for now)
    if len(text) < 1:
        pass

    # try to open a file and write text into
    try:
        # open the file
        with open(fileName, write_mode) as fileToEdit:
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


# cd to a directory
def __change_user_directory__(command, chat_id):
    # if no args are provided
    if len(command) == 0:
        # cd to main path
        newpath = main_path
    # if address is independant
    elif command.startswith('/'):
        # change address straightly
        newpath = os.path.realpath(command)
    # if address is relative
    else:
        # change address relative to the current path
        newpath = os.path.realpath(users_directories[chat_id] + '/' + command)
    
    # if the given path exists
    if os.path.exists(newpath):
        # change user directory to the path
        users_directories[chat_id] = newpath
    # if path does not exist
    else:
        # do not change directory. return error message.
        return 'Error path does not exist'
    
    # if it was susccessful, return current path
    return users_directories[chat_id]


# a dict of special commands mapped to corresponding function
special_commands = {
    '/sh':__run_sh__,
    '/edit':__edit_file__,
    '/send':__send_file__,
    '/help': __print_help_message__,
    '/ps': __show_process_list__,
    'cd': __change_user_directory__,

}

