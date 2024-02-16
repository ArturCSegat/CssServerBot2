import socket


def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("69.69.69.69", 80))
    n = s.getsockname()[0]
    s.close()
    return n
