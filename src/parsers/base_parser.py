from abc import abstractmethod
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from logger import setup_logging
import os


setup_logging()

chrome_options = Options()
# chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
# hide browser
chrome_options.add_argument("--headless")

PAGE_LOAD_TIMEOUT_S = 60
CUR_DIR = os.path.dirname(__file__)


class BaseParser():
    def __init__(self, symbol, url) -> None:
        self.driver = Chrome(chrome_options=chrome_options, executable_path=f"{CUR_DIR}/../../driver/chromedriver")
        # stop loading page after PAGE_LOAD_TIMEOUT_S
        self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT_S)
        self.url = url
        self.symbol = symbol

    def __delete__(self):
        self.driver.close()

    @abstractmethod
    def get_data() -> dict:
        raise NotImplementedError
