import subprocess

# run command using sh shell
def __run_sh__(command : str):
    # run command using sh shell
    return subprocess.check_output(command, shell=True)

# print a text into a file
def __edit_file__(command : str):
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


# a dict of special commands mapped to corresponding function
special_commands = {
    '/sh':__run_sh__,
    '/edit':__edit_file__
}

