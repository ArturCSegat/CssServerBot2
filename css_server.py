from subprocess import Popen
from rcon import Rcon, RconError, RconType
from file_utils import valid_srcds_path

class Server:
    __process: Popen
    __rcon: Rcon
    __map: str

    def __new__(cls, path: str, ip: str, port: int, passwd: str) -> 'Server | RconError | OSError':
        self =  super().__new__(cls)

        if path != "":
            validation = valid_srcds_path(path)
            if validation is not None:
                return validation

            try:
                self.__process = Popen([f"{path}/srcds.exe",  "-console", "-game", "cstrike", "-secure", "+map", "cs_office", "-autoupdate", "+log", "on", "+maxplayers",  "32", "-port", str(port), "+ip", str(ip), "+exec", "server.cfg"])
            except OSError as e:
                print('porra')
                return e 

        con = Rcon(ip, port, passwd)
        if not isinstance(con, Rcon):
            return con
        self.__rcon = con

        self.__map = "bosta"
        return self

    def change_level_to(self, map: str) -> str:
        if map == self.__map:
            return "bad map"
        r = self.__rcon.send_command(f"changelevel {map}", RconType.SERVERDATA_EXECCOMMAND)
        if isinstance(r, str):
            return r
        return "bad command"

    def run(self, cmd: str) -> str:
        r = self.__rcon.send_command(cmd, RconType.SERVERDATA_EXECCOMMAND)
        if isinstance(r, str):
            return r
        return "bad command"

    def __del__(self):
        if self.__process:
            self.__process.kill()

