from collections import UserDict
import subprocess
import requests
from config import bot_token, users_directories, main_path, help_file_name, chatid_users, sudoers_chatid, user_running_bot
import pickle
import os, pwd, stat
from io import StringIO 
import sys
from variables import pidlist

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


"""
    what we need:
    check uid, gid, mode for a file
    check if a uid is in a gid
    check mod for the uid or gid or others.
"""

def check_file_permission(filename:str, chat_id) -> list:

    username = chatid_users[chat_id]

    # user_access_mode is a subset of ['read', 'write', 'exec']
    user_access_mode = []

    # if user is the user running the bot, then the os will return good answer
    if username == user_running_bot or (username in sudoers_chatid and user_running_bot == 'root'):
        if os.access(filename, os.R_OK):
            user_access_mode.append('read')
        if os.access(filename, os.W_OK):
            user_access_mode.append('write')
        if os.access(filename, os.X_OK):
            user_access_mode.append('exec')
        
        # job is done!
        return user_access_mode
    
    # but if username is not the same as robot user:
    
    # get file uid, gid, mode
    file_user_id = os.stat(filename).st_uid
    file_access_mode_code = os.stat(filename).st_mode
    file_access_mode = stat.filemode(file_access_mode_code)
    user_uid = pwd.getpwnam(username).pw_uid

    # support for group access is not implemented yet. TODO
    if user_uid == file_user_id:
        if file_access_mode[1] == 'r':
            user_access_mode.append('read')
        if file_access_mode[2] == 'w':
            user_access_mode.append('write')
        if file_access_mode[3] == 'x':
            user_access_mode.append('exec')
    else:
        if file_access_mode[7] == 'r':
            user_access_mode.append('read')
        if file_access_mode[8] == 'w':
            user_access_mode.append('write')
        if file_access_mode[9] == 'x':
            user_access_mode.append('exec')

    return user_access_mode


# run command using sh shell
def __run_sh__(command : str, chat_id):


    username = chatid_users[chat_id]
    sh_filename = f'{main_path}/user_{username}_shell_command_to_run.sh'

    with open(sh_filename, 'w') as cmdfile:
        cmdfile.write('#!/usr/bin/bash\n')
        cmdfile.write(command)
                    
        os.chmod(sh_filename, 0o777)

    if user_running_bot == 'root':

        username = chatid_users[chat_id]

        command_to_run = f'runuser -u {username} {sh_filename}'
        # command_to_run = f'runuser -u {username} ' + command
    else:
        command_to_run = command

    print(command_to_run)
    # run command using sh shell
    text = subprocess.check_output(command_to_run, shell=True)
    os.chdir(users_directories[chat_id])

    return text


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
            filename = arg
            break

    if 'write' not in check_file_permission(filename, chat_id):
        return 'you do not have permission'

    # if we remove first line from the message, remaining will be text body of file
    text = command[len(command.split('\n')[0])+1:]

    # if text is empty, do nothing. (there is some reason for now)
    if len(text) < 1:
        pass

    # try to open a file and write text into
    try:
        # open the file
        with open(filename, write_mode) as fileToEdit:
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

    # check user permission
    if 'read' not in check_file_permission(filename, chat_id):
        return 'you do not have permission'

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

    # go to directory where help file is stored

    with open(help_file_name) as help_file:
        help_text = help_file.read()

    message = {
        "chat_id":chat_id,
        # "parse_mode":"MarkdownV2",
        "text":help_text,
    }

    # requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data=message)
    return help_text


# todo. this is just a temporary solution!!!
def __show_process_list__(command, chat_id):
    text = ''
    for i, process_info in enumerate(pidlist):
        print(i, process_info)
        text += str(i) + ' 🥕 ' + str(process_info[0]) + ' ' + process_info[1] + '\n'
    # text = '🥕 ' + '\n🥕 '.join([str(pid[0]) + ' ' + pid[1] for pid in pidlist])
    if len(text) < 1:
        text = '🥕 there is no process running'
    return text

def __kill_process_index__(command, chat_id):
    process_index = int(command)
    proc = pidlist[process_index][2]
    proc.kill()
    pidlist.remove(pidlist[process_index])
    return 'killed'

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

# receive file sent to chat and store it on the server
def __receive_file__(command, chat_id):
    
    # we have to get (file_name, file_path, chat_id) from where it was stored TODO
    
    os.chdir(main_path)
    try:
        users_file_paths = pickle.load(open('users_file_paths.pickle', 'rb'))
    except FileNotFoundError:
        return 'there was an error. send a file (or resend it)'
    
    file_name, file_path = users_file_paths[chat_id]


    # send a request and get the file itself.
    fileData = requests.get(f'https://api.telegram.org/file/bot{bot_token}/{file_path}')

    # if there are args
    if len(command) > 0:
        # change file name into what was provided.
        file_name = command

    # change dir to where user was in (for relative file names)
    os.chdir(users_directories[chat_id])
    # open a new file for writing into and write file content into it
    open(file_name, 'wb').write(fileData.content)
    # return file name and path as a success message
    return os.path.realpath(users_directories[chat_id] + '/' + file_name)


def __run_as_sudo_shell__(command, chat_id):
    if chat_id in sudoers_chatid:

        # run command using sh shell
        text = subprocess.check_output(command, shell=True)
    
    else:
        text = 'you are not a sudoer!'

    return text

def __execute_python_code__(command, chat_id):
    username = chatid_users[chat_id]
    if username == user_running_bot or (user_running_bot == 'sudo' and chat_id in sudoers_chatid):
        with Capturing() as output:
            exec(command)
        return repr(output)
    else:
        return 'you are not allowed to use this command!'

# a dict of special commands mapped to corresponding function
special_commands = {
    '/sh':__run_sh__,
    '/edit':__edit_file__,
    '/send':__send_file__,
    '/help': __print_help_message__,
    '/ps': __show_process_list__,
    'cd': __change_user_directory__,
    '/receive': __receive_file__,
    '/sudo':__run_as_sudo_shell__,
    '/exec': __execute_python_code__,
}

