import os
import requests
import rarfile
import zipfile
import shutil
import py7zr as sz

def valid_srcds_path(path: str) -> OSError | None:
    if not os.path.isdir(path):
        return OSError("invalid path: is not a directory")
    if not "srcds.exe" in os.listdir(path):
        return OSError("invalid path: does not contain srcds.exe")
    if not "cstrike" in os.listdir(path):
        return OSError("does not have cs source installed in source dedicated server")

def valid_map(map_name: str, maps_dir_path: str) -> OSError | None:
    if not os.path.isdir(maps_dir_path):
        return OSError("path to maps directory is not a real directory")
    map_file = map_name + ".bsp"
    if not map_file in os.listdir(maps_dir_path):
        return OSError("Map Not found")

def download_zip_file(url, path) -> OSError | None:
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(path, 'wb') as f:
            try:
                i = f.write(response.content)
                if i < 0:
                    return OSError(f"Could no write to file path: {path}")
            except OSError as e:
                return e
    else:
        return  OSError(f"Could not donwload map from url {url}")


def extract_bsp(compressed_path, outputfolder="./") -> OSError | str:
    if rarfile.is_rarfile(compressed_path):
        rar = rarfile.RarFile(compressed_path)
        for fil in rar.infolist(): # checks fot the bsp in any depth
            if fil.filename.endswith('.bsp'):
                rar.extract(fil.filename, outputfolder)

                # if the bsp was in a folder inside the arquvie it would extract the folder with it, this extracts it from
                # the folder it came from and than deletes the folder
                file_name = os.path.basename(fil.filename)
                parent_dir = os.path.dirname(fil.filename)
                if parent_dir != '':
                    shutil.move(f"{outputfolder}/{parent_dir}/{file_name}", f"{outputfolder}/{file_name}")
                    os.rmdir(f"{outputfolder}/{parent_dir}")

                return str(os.path.basename(fil.filename))
        os.remove(compressed_path)
        return OSError("Invalid rar archive no bsp file")
    elif zipfile.is_zipfile(compressed_path):
        zi = zipfile.ZipFile(compressed_path)
        for fil in zi.infolist():
            if fil.filename.endswith('.bsp'):
                zi.extract(fil.filename, outputfolder)

                file_name = os.path.basename(fil.filename)
                parent_dir = os.path.dirname(fil.filename)
                if parent_dir != '':
                    shutil.move(f"{outputfolder}/{parent_dir}/{file_name}", f"{outputfolder}/{file_name}")
                    os.rmdir(f"{outputfolder}/{parent_dir}")
                return str(os.path.basename(fil.filename))
    elif sz.is_7zfile(compressed_path):
        zi = sz.SevenZipFile(compressed_path)
        for fil in zi.list():
            if fil.filename.endswith('.bsp'):
                zi.extract(fil.filename, outputfolder)

                file_name = os.path.basename(fil.filename)
                parent_dir = os.path.dirname(fil.filename)
                if parent_dir != '':
                    shutil.move(f"{outputfolder}/{parent_dir}/{file_name}", f"{outputfolder}/{file_name}")
                    os.rmdir(f"{outputfolder}/{parent_dir}")
                return str(os.path.basename(fil.filename))
        return OSError("Invalid zip archive no bsp file")
    else: # could modify this to raise an exepton but lol
        return OSError("archive type not suported")

