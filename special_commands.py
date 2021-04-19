import subprocess

def __run_sh__(command):
    return subprocess.check_output(command, shell=True)


special_commands = {
    '/sh':__run_sh__,
}

