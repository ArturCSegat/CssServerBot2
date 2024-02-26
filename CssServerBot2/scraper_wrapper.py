from subprocess import Popen, PIPE
import file_utils

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

        self.__last_map_request = str(scrapper_process.stdout.readline())
        self.__last_map_url = str(scrapper_process.stdout.readline())
        self.__last_download_url = str(scrapper_process.stdout.readline())

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
        error = file_utils.download_zip_file(self.__last_download_url, f"{out_dir}/{self.__last_map_request}.zip")
        if error is not None:
            return error
        out = file_utils.extract_bsp(f"{out_dir}/{self.__last_map_request}.zip", out_dir)
        if isinstance(out, OSError):
            return out

