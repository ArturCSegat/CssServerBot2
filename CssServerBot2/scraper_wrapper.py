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
        print(self.__last_map_request)
        print(self.__last_map_url)
        print(self.__last_download_url)
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
        return file_utils.save_map(out_dir, self.last_map_name(), self.last_map_download_url())

def remove_cr(s: str) -> str:
    n = ""
    for c in s:
        if c == '\n':
            continue
        n += c
    return n