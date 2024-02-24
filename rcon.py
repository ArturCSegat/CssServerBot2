from socket import socket, AF_INET, SOCK_STREAM, error as sock_err
from enum import Enum
import struct
import random

class RconType(Enum):
    SERVERDATA_EXECCOMMAND = 2
    SERVERDATA_AUTH = 3

class RconAuthError(Exception):
    def __init__(self, msg="Bad Auth in RCON"):
        super().__init__(msg)

RconSockError = sock_err

class RconError(Enum):
     SockError = RconSockError
     AuthError = RconAuthError

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
            return RconError.SockError
        
        auth = self.auth()
        if auth is not None:
            return auth

        return self

    def auth(self) -> None | RconError:
        try: 
            self.send_command(self.passwd, RconType.SERVERDATA_AUTH)
            bs = self.sock.recv(4)
            id = int.from_bytes(bs, byteorder="little")
        except sock_err:
            return RconError.SockError

        if id == -1:
            return RconError.AuthError
        return None

    def send_command(self, body: str, type: RconType) -> int | RconSockError:
        id = random.randint(1, 99999)
        size = len(body) + 10

        buffer = struct.pack('<iii', size, id, type.value) + body.encode() + bytes([0, 0])
        try:
            return self.sock.send(buffer)
        except sock_err as e:
            return e


