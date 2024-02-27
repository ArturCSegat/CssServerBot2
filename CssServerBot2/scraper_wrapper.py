from subprocess import Popen, PIPE
import file_utils
import os

class GameBananaScraper():
    __last_map_url: str
    __last_download_url: str
    __last_map_request: str

    def __init__(self):
        self.__last_map_url = ""
        self.__last_download_url = ""
        self.__last_map_request = ""
        pass

    def scrape(self, map_request: str) -> bool:
        try:
            scrapper_process = Popen(['node', '../scraper/gamebanana_scraper.js', map_request], stdout=PIPE)
        except:
            return False

        if scrapper_process.stdout is None:
            return False

        self.__last_map_request = remove_cr(scrapper_process.stdout.readline().decode())
        self.__last_map_url = remove_cr(scrapper_process.stdout.readline().decode())
        self.__last_download_url = remove_cr(scrapper_process.stdout.readline().decode())

        return True

    def last_map_name(self):
        return self.__last_map_request
    def last_map_url(self):
        return self.__last_map_url
    def last_map_download_url(self):
        return self.__last_download_url

    def save(self, out_dir: str) -> OSError | None:
        """
            game banana may save maps in .rar or .zip, in our case if we get a .rar file, we well endup
            renaming it to .zip, but rarfile.israrfile() does not check via file name, so its fine
        """
        out_file =  f"{out_dir}/{self.__last_map_request}.zip"
        error = file_utils.download_zip_file(self.__last_download_url, out_file)

        if error is not None:
            os.remove(out_file)
            return error
        out = file_utils.extract_bsp(out_file, out_dir)
        if isinstance(out, OSError):
            os.remove(out_file)
            return out
        os.remove(out_file)

def remove_cr(s: str) -> str:
    n = ""
    for c in s:
        if c == '\n':
            continue
        n += c
    return n