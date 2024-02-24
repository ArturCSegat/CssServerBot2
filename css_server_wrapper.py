from subprocess import Popen
import os

from .rcon import Rcon, RconError, RconType
from .ip_utils import get_local_ip

PATH = os.getenv("SRCDS_PATH")
if PATH is None:
    print("set the SRCDS_PATH env variable")
    exit(1)
PORT = os.getenv("PORT")
if PORT is None:
    PORT = 27015
PORT = int(PORT)
IP = os.getenv("IP")
if IP is None:
    IP = get_local_ip()
PASSWD = os.getenv("RCON_PASSWD")
if PASSWD is None:
    print("must set the RCON_PASSWD env variable")
    exit(1)

class Server:
    def __init__(self):
        self.__process: Popen = Popen([
            f"{PATH} -console -game cstrike -secure +map cs_office -autoupdate +log on +maxplayers 32 -port {PORT} +ip {IP} +exec server.cfg\n"
            ])
        con: Rcon | RconError = Rcon(IP, PORT, PASSWD)
        if not isinstance(con, Rcon):
            # TODO
            print("TODOOOO")
            exit(1)
        self.__rcon = con

        if self.__process.stdin is None or self.__process.stdout is None:
            exit(1)

        self.map: str = "bosta"

    def change_level_to(self, map: str) -> None:
        if map == self.map:
            return

        self.__rcon.send_command(f"changelevel {map}\n", RconType.SERVERDATA_EXECCOMMAND)
