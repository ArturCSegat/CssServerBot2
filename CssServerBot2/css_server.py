from subprocess import Popen
import typing
from rcon import Rcon, RconError, RconType
from file_utils import valid_srcds_path, valid_map

class ServerMapError(Exception):
    def __init__(self, msg="Error: Error happened in the CS server") -> None:
        super().__init__(msg)
class ServerCommandError(Exception):
    def __init__(self, msg="Error: Error happened in the CS server") -> None:
        super().__init__(msg)

ServerError = typing.Union[ServerMapError, ServerCommandError]

class CssServer:
    __process: Popen
    __rcon: Rcon
    __map: str
    __path: str
    __ip: str
    __port: int

    def __new__(cls, path: str, ip: str, port: int, passwd: str) -> 'CssServer | RconError | OSError':
        self =  super().__new__(cls)
        
        self.__ip = ip
        self.__path = path
        self.__port = port
        
        if path != "":
            validation = valid_srcds_path(path)
            if validation is not None:
                return validation

            try:
                self.__process = Popen([f"{path}/srcds.exe",  "-console", "-game", "cstrike", "-secure", "+map", "cs_office", "-autoupdate", "+log", "on", "+maxplayers",  "32", "+port", str(port), "+exec", "server.cfg"])
            except OSError as e:
                print(f"{path}/srcds.exe")
                return e 

        con = Rcon(ip, port, passwd)
        if not isinstance(con, Rcon):
            return con
        self.__rcon = con

        self.__map = "bosta"
        return self

    def change_level_to(self, map: str) -> str | ServerError:
        if map == self.__map:
            return ServerMapError("This Map is already selected")
        validation = valid_map(map, self.__path + "/cstrike/maps")

        if validation is not None:
            return ServerMapError(validation.__str__())
        
        r = self.__rcon.send_command(f"changelevel {map}", RconType.SERVERDATA_EXECCOMMAND)
        if isinstance(r, str):
            return r
        return ServerCommandError("The command could not be issued to the server")

    def run(self, cmd: str) -> str | ServerCommandError:
        r = self.__rcon.send_command(cmd, RconType.SERVERDATA_EXECCOMMAND)
        if isinstance(r, str):
            return r
        return ServerCommandError("The command could not be issued to the server")

    def __del__(self):
        if self.__process:
            self.__process.kill()

