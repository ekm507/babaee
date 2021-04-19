import subprocess

# run command using sh shell
def __run_sh__(command):
    # run command using sh shell
    return subprocess.check_output(command, shell=True)


# a dict of special commands mapped to corresponding function
special_commands = {
    '/sh':__run_sh__,
}

