# babaee
a telegram bot for remote controlling a server

## how to use

1. create a telegram bot and note the bot token
2. clone this repository on the server
3. in `config.py` file, set robot token and your chat_id.
4. run the bot:
```bash
python3 babaee.py
```

## TODO

- let user to append into file using `/edit` command.
- show a list of running subprocesses with a killing ability. (temporary solution: linux ps command)
- make an interface for other apps to let them communicatie with admin via telegram.
- make better logs.
- send files. (sending files from server on telegram is possible now. opposite is not.)
