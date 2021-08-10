from logger import setup_logging
import logging as logger
from parsers.base_parser import BaseParser
from datetime import datetime
import traceback
import requests
import re
import json

setup_logging()


class VietcombankParser(BaseParser):
    def __init__(self, symbol, url) -> None:
        super().__init__(symbol, url)

    def get_data(self) -> dict:
        try:
            logger.info(f"Loading url = {self.url} ..")
            response = requests.get(self.url)
            logger.info("Page is loaded!")

            result = re.findall(r"json_parse=JSON.parse\('(.*?)'\)", response.text)
            json_data = result[0]
            # logger.info(json_data)
            data = json.loads(json_data)
            # logger.info(data)
            return self.standardize_time(data)
        except Exception as e:
            traceback.print_exc()
            logger.error(e)
            return None

    def standardize_time(self, data: list) -> dict:
        result = dict()
        for item in data:
            day = int(item['d'])
            month = int(item['m'])
            year = int(item['Y'])
            date = datetime(year=int(year), month=int(month), day=int(day))
            result[int(date.timestamp() * 1000)] = int(item['price'])

        return result
