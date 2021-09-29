# babaee
a telegram bot for remote controlling a server

## how to use

there are two ways to run this robot.  
one by a non-root user  
other by root user.

when run by non-root user, commands will be run as your user.

when run by root user, you can define users for each person interacting with robot. you will also give users root access for running commands.

thus, the way you run the robot, you need to configure it differently.

### configure for non-root user


### configure for root user

1. create a telegram bot and note the bot token
2. clone this repository on the server
3. copy `config.py.default` into `config.py` file.
4. in `config.py` file set robot token and your `chat_id`.
5. run the bot:

### running the robot

``` bash
python3 babaee.py
```

## TODO

- show a list of running subprocesses with a killing ability. (temporary solution: linux ps command)
- make an interface for other apps to let them communicatie with admin via telegram.
- make better logs. (how should they be?)
- run commands in with user access
- option to reply to messages when answering. for avoiding out of order outputs