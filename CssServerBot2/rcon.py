from socket import socket, AF_INET, SOCK_STREAM, error as sock_err
from enum import Enum
import struct
import random
import typing

class RconType(Enum):
    SERVERDATA_EXECCOMMAND = 2
    SERVERDATA_AUTH = 3

class RconAuthError(Exception):
    def __init__(self, msg="Bad Auth in RCON"):
        super().__init__(msg)
RconSockError = sock_err

RconError = typing.Union[RconSockError, RconAuthError]

class Rcon:
    ip: str
    port: int
    passwd: str
    sock: socket

    def __new__(cls, ip: str, port: int, passwd: str) -> 'Rcon | RconError':
        self = super().__new__(cls)
        self.ip = ip
        self.port = port
        self.passwd = passwd
        
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect((self.ip, self.port))
        except sock_err:
            return RconSockError("Could not open socket to rcon server")
        
        auth = self.auth()
        if auth is not None:
            return auth

        return self

    def auth(self) -> None | RconError:
        try: 
            """
                Weird ness is caused becaused after auth, server will respondo with emppty package, and then ith real package, of
                wich we only care about the id
            """
            self.send_command(self.passwd, RconType.SERVERDATA_AUTH, returncontent=False)
            bs = self.sock.recv(4)
            size = int.from_bytes(bs, byteorder="little")
            _ = self.sock.recv(size) # ignore empty response
            size = int.from_bytes(self.sock.recv(4), byteorder="little") # get size of real
            bsid = self.sock.recv(4) # get bytes of id
            _ = self.sock.recv(size - 4) # ignore rest
        except sock_err as e:
            return RconSockError(e.__str__())

        if bsid == bytes([0xff, 0xff, 0xff, 0xff]):
            return RconAuthError("Received negative response from server, bad password")
        return None

    """
        body: content to be sent
        type: RCON type, probrably EXECCOMMAND
        returncontent: set to false if you wish to handle your own response
    """
    def send_command(self, body: str, type: RconType, returncontent=True) -> str | RconSockError:
        id = random.randint(1, 99999)
        size = len(body) + 10

        buffer = struct.pack('<iii', size, id, type.value) + body.encode() + bytes([0, 0])
        try:
            self.sock.send(buffer)
            if returncontent is False:
                return ""
            size = int.from_bytes(self.sock.recv(4), byteorder="little") # read size
            _ = self.sock.recv(4) # ignore id
            _ = self.sock.recv(4) # ignore type
            cont = self.sock.recv(size - 8) # read content
            if cont == b'\0\0':
                return ""
            return str(cont)

        except sock_err as e:
            return e


