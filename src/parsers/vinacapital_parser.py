from logger import setup_logging
import logging as logger
from parsers.base_parser import BaseParser
from datetime import datetime
import traceback

setup_logging()


class VinaCapitalParser(BaseParser):
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
            var data = visualizer.charts;
            var key = Object.keys(data)[0];
            var data = data[key].data;

            chartData = []
            for (let i=0; i<data.length; i++) {
                d = data[i][0]
                day = d.getDate()
                month = d.getMonth() + 1
                year = d.getFullYear()
                price = Math.floor(data[i][1])
                chartData.push(day +"/"+month+"/"+year + "," + price)
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
