import subprocess

# run command using sh shell
def __run_sh__(command):
    # run command using sh shell
    return subprocess.check_output(command, shell=True)

def __edit_file__(command : str):
    fileName = command.split(' ')[0].split('\n')[0]
    text = command[len(fileName)+1:]
    if len(text) < 1:
        pass
    try:
        with open(fileName, 'w') as fileToEdit:
            fileToEdit.write(text)
        return 'File edited successfully'
    except:
        return 'Error: there was an error editing file'


# a dict of special commands mapped to corresponding function
special_commands = {
    '/sh':__run_sh__,
    '/edit':__edit_file__
}

