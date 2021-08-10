from logger import setup_logging
import logging as logger
from parsers.base_parser import BaseParser
from datetime import date
import traceback
import requests
import json

setup_logging()


class VnIndexParser(BaseParser):
    def __init__(self, symbol, url) -> None:
        super().__init__(symbol, url)
        self.limit = 1000
        self.end_date = date.today().strftime('%d/%m/%Y')
        self.url = f"{url}&date_ended={self.end_date}"

    def get_data(self) -> dict:
        try:
            logger.info(f"Loading url = {self.url} ..")
            response = requests.get(self.url)
            data = json.loads(response.text)
            vnindex = data['chartCompareData']['data']
            return self.standardize_time(vnindex)
        except Exception as e:
            traceback.print_exc()
            logger.error(e)
            return None

    def standardize_time(self, data: list) -> dict:
        result = dict()
        for item in data:
            time = item[0]
            price = item[1]
            # d = datetime.fromtimestamp(time / 1000)
            # date_str = d.strftime('%d/%m/%Y')
            result[int(time)] = int(price)

        return result
