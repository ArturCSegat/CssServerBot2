from socket import socket, AF_INET, SOCK_STREAM
from enum import Enum
import struct
import random

class RconType(Enum):
    SERVERDATA_EXECCOMMAND = 2
    SERVERDATA_AUTH = 3

class Rcon:
    def __init__ (self, ip: str, port: int, passwd: str):
        self.ip = ip
        self.port = port
        self.passwd = passwd
        
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.ip, self.port))

        self.auth()

    def auth(self):
        self.send_command(self.passwd, RconType.SERVERDATA_AUTH)

    def send_command(self, body: str, type: RconType):
        id = random.randint(1, 99999)
        size = len(body) + 10

        buffer = struct.pack('<iii', size, id, type) + body.encode() + bytes([0, 0])

        self.sock.send(buffer)


