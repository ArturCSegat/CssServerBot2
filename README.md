# CssServerBot2
## Rcon wrapper to handle Counter Strike Source server from a discord bot

# Usage

## Windows

`git clone https://github.com/ArturCSegat/CssServerBot2`

`set TOKEN=<your discord bot token>`

`set IP=<ip of your server, if empty will get yout local ip>`

`set PORT=<port of your server, defaults to 27015>`

`set RCON_PASSWD=<your Rcon password, you should set it in server.cfg>`

`set SRCDS_PATH=<the path to the folder that contains your srcds.exe file, if left empty, will look for a exisiting server in the provided IP>`

`python main.py`


## Linux and Mac

`git clone https://github.com/ArturCSegat/CssServerBot2`

`export TOKEN="<your discord bot token>"`

`export IP="<ip of your server, if empty will get yout local ip>"`

`export PORT="<port of your server, defaults to 27015>"`

`export RCON_PASSWD="<your Rcon password, you should set it in server.cfg>"`

`export SRCDS_PATH="<the path to the folder that contains your srcds.exe file, if left empty, will look for a exisiting server in the provided IP>"`

`python3 main.py`

