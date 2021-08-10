from logger import setup_logging
import logging as logger
from parsers.base_parser import BaseParser
import traceback
from urllib import request
from xlsx2csv import Xlsx2csv
from csv import reader
from datetime import datetime


setup_logging()


class SSIParser(BaseParser):
    def __init__(self, symbol, url) -> None:
        super().__init__(symbol, url)
        self.xlsx_temp_file = f"/tmp/{symbol}.xlsx"
        self.csv_temp_file = f"/tmp/{symbol}.csv"

    def get_data(self) -> dict:
        try:
            logger.info(f"Loading url = {self.url} ..")
            request.urlretrieve(self.url, self.xlsx_temp_file)
            logger.info(f"Saved data to temp file {self.xlsx_temp_file} . Converting data to csv ...")
            Xlsx2csv(self.xlsx_temp_file, outputencoding="utf-8").convert(self.csv_temp_file)
            logger.info(f"Converted data to temp file {self.csv_temp_file}")
            # skip first line i.e. read header first and then iterate over each row od csv as a list
            data = []
            with open(self.csv_temp_file, 'r') as read_obj:
                csv_reader = reader(read_obj)
                header = next(csv_reader)
                # Check file as empty
                if header is not None:
                    # Iterate over each row after the header in the csv
                    for row in csv_reader:
                        # row variable is a list that represents a row in csv
                        data.append((row[2], row[3]))
            data.reverse()
            return self.standardize_time(data)
        except Exception as e:
            traceback.print_exc()
            logger.error(e)
            return None

    def standardize_time(self, data: list) -> dict:
        result = dict()
        for (date, price) in data:
            price, _ = price.split(',')
            price = price.replace('.', '')
            day, month, year = date.split('/')
            date = datetime(year=int(year), month=int(month), day=int(day))
            result[int(date.timestamp() * 1000)] = int(price)

        return result
