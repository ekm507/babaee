# babaee
a telegram bot for remote controlling a server

it is the system-admins's assistant telegram bot!

## how to set up a _babaee_ on your server

this is a pretty straightforward guide for setting up your own *babaee* robot.

1. clone this repository.
2. copy `config.py.default` into `config.py`.
3. configure `config.py`.
3. run robot with command `python3 babaee.py`.

## more details on how to set up _babaee_

### prerequisits


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

when run by root user, you can define users for each person interacting with robot. you may also give users root access for running commands.

thus, the way you run the robot, you need to configure it differently.

### configure for non-root user


edit `config.py` file.

1. edit `robot_token`

     in `config.py` file set robot token
    ```python
    robot_token = "token you get from botfather"
    ```

2. edit `admins_chat_id_list`.

    add your `chat_id` (you can add several ones)

    as an example:
    ```python
    # chat id of admins
    admins_chat_id_list = [
        12121212,
        13131313,
        # integer
    ]

    ```

3. edit `forward_chat_id_list`

    it is possible to send a log from users commands to a telegram user.

    for example:

    ```python
    # a list of chat id. bot will forward all incoming messages to these users.
    forward_chat_id_list = [
        12121212,
        # integers
    ]
    ```



### configure for root user

edit `config.py` file.

1. edit `robot_token`

     in `config.py` file set robot token
    ```python
    robot_token = "token you get from botfather"
    ```

2. edit `admins_chat_id_list`.

    add your `chat_id` (you can add several ones)

    as an example:
    ```python
    # chat id of admins
    admins_chat_id_list = [
        12121212,
        13131313,
        # integer
    ]

    ```

3. edit `chatd_users` dict.

    each chat_id must be assigned to a user on your machine.

    as an example:

    ```python
    chatid_users = {
        12121212:'erfan',
        13131313:'funny-user'
        # integer:string
    }
    ```

4. edit `sudoers_chatid` list

    it is possible to give a user root access.

    for example if you want to let user 12121212 be able ro run commands as root:"

    ```python
    sudoers_chatid = [
        12121212,
        #integer
    ]
    ```

5. edit `forward_chat_id_list`

    it is possible to send a log from users commands to a telegram user, for instance root user's telegram.

    for example:

    ```python
    # a list of chat id. bot will forward all incoming messages to these users.
    forward_chat_id_list = [
        12121212,
        # integers
    ]
    ```

### running the robot

run the bot using python3

``` bash
python3 babaee.py
```

## usage

to use the bot, simply type linux commands in it.  
however there are some special commands you can use.

### special commands

- /help : robot help
- /sh : run command in shell
- /sudo : run command as root in shell
- /send : send a file from server to telegram
- /receive : receive a file from telegram into server
- /edit : edit a file
- /ps : list of running processes


## TODO

- show a list of running subprocesses with a killing ability. (temporary solution: linux ps command)
- make an interface for other apps to let them communicatie with admin via telegram.
- make better logs. (how should they be?)
- write a better help file
- make a cli for configuration
- split telegram interface from the main code into a different file. this way robot can be used for other platforms, also testing can be easier.
