from subprocess import Popen, PIPE


class Server:
    def __init__(self, ip: str):
        # REAL
        # self.process: Popen = Popen(["C:\\css\\srcds.exe"], stdin=PIPE, stdout=PIPE)

        # FAKE
        self.process: Popen = Popen(["python3", "css.py"], stdin=PIPE, stdout=PIPE)

        if self.process.stdin is None or self.process.stdout is None:
            exit(1)

        # self.process.stdin.write(bytes(f"-console -game cstrike -secure +map cs_office -autoupdate +log on +maxplayers 32 -port 27015 +ip {ip} +exec server.cfg\n", "utf-8"))

        self.map: str = "bosta"

    def change_level_to(self, map: str) -> None:
        if map == self.map:
            return
        if self.process.stdin is None or self.process.stdout is None:
            return

        self.process.stdin.write(bytes(f"changelevel {map}\n", "utf-8"))
        self.process.stdin.flush()

    def __del__(self):
        print(str(self.process.communicate()))
