# babaee
a telegram bot for remote controlling a server

## how to use

this is a pretty straightforward guide for setting up your own *babaee* robot.

### prerequirements


1. create a telegram bot and note the bot token. ([here is how to do it](https://core.telegram.org/bots#3-how-do-i-create-a-bot))
2. clone this repository on the server

```bash
git clone 'https://github.com/ekm507/babaee.git'

```

3. copy `config.py.default` into `config.py` file.
```bash
cp config.py.default config.py
```

### edit the `config.py` file

there are two ways to run this robot.  
1. by a non-root user  
2. by root user.

when run by non-root user, commands will be run as your user.

when run by root user, you can define users for each person interacting with robot. you will also give users root access for running commands.

thus, the way you run the robot, you need to configure it differently.

### configure for non-root user



### configure for root user
1. in `config.py` file set robot token
```python
robot_token = "token you get from botfather"
```

2. and your `chat_id` (you can add several ones)
```python

```
2. run the bot:

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