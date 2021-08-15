from logger import setup_logging
import logging as logger
from parsers.base_parser import BaseParser
from datetime import datetime
import traceback

setup_logging()


class DaichiParser(BaseParser):
    def __init__(self, symbol, url) -> None:
        super().__init__(symbol, url)

    def get_data(self) -> dict:
        try:
            logger.info(f"Loading url = {self.url} ..")
            try:
                self.driver.get(self.url)
            except Exception as e:
                logger.info(e)

            logger.info("Page is loaded!")

            script = """
            var last_key = Object.keys(charts)[Object.keys(charts).length-1];
            var data = charts[last_key];
            var chartData = [];
            for (let i=1; i<data.length; i++) {
                item = data[i];
                var d = new Date(item[0]*1000);
                day = d.getDate();
                month = d.getMonth() + 1;
                year = d.getFullYear();
                price = Math.floor(item[7]);
                chartData.push(day+ "/" + month + "/" +  year + "," + price);
            }
            return chartData;

            """

            logger.info("Parse data ...")

            result = self.driver.execute_script(script)
            # logger.info(result)
            return self.standardize_time(result)
        except Exception as e:
            traceback.print_exc()
            logger.error(e)
            return None

    def standardize_time(self, data: list) -> dict:
        result = dict()
        for item in data:
            time, price = item.split(',')
            day, month, year = time.split('/')
            date = datetime(year=int(year), month=int(month), day=int(day))
            result[int(date.timestamp() * 1000)] = int(price)

        return result
