import os

def valid_srcds_path(path: str) -> OSError | None:
    if not os.path.isdir(path):
        return OSError("invalid path: is not a directory")
    if not "srcds.exe" in os.listdir(path):
        return OSError("invalid path: does not contain srcds.exe")
    if not "cstrike" in os.listdir(path):
        return OSError("does not have cs source installed in source dedicated server")
