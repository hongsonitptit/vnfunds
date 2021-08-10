from logger import setup_logging
import logging as logger
from datetime import datetime
from parsers.base_parser import BaseParser
import traceback

setup_logging()


class DragonCapitalParser(BaseParser):
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
            var chartData = {};
            Highcharts.charts[0].series.map(function(chartContents, ix) {
                chartData[ix] = {
                    "name": chartContents.name,
                    "time_list" : chartContents.xData,
                    "price_list": chartContents.yData
                }
            });
            return chartData;
            """

            # script = """
            # var arr = Highcharts.charts[0].series[0].data;
            # var chartData = [];
            # for (let i=0; i<arr.length; i++) {
            #     if (typeof arr[i] !== "undefined") {
            #         chartData.push(arr[i].category + "," + arr[i].y);
            #     }
            # }
            # return chartData;
            # """

            logger.info("Parse data ...")

            result = self.driver.execute_script(script)
            for _, value in result.items():
                name = value['name']
                if name != self.symbol:
                    continue
                time_list = value['time_list']
                price_list = value['price_list']
                price_history = self._parse_price_history(time_list, price_list)
                return price_history
        except Exception as e:
            traceback.print_exc()
            logger.error(e)
            return None

    def _standardize_time(self, epoch_time: int) -> str:
        # convert epoch_time in second
        while len(str(epoch_time)) > 10:
            epoch_time = int(epoch_time / 1000)
        date = datetime.fromtimestamp(epoch_time)
        return date.strftime('%d/%m/%Y')

    def _parse_price_history(self, time_list, price_list) -> dict:
        price_history = dict()
        for i in range(len(time_list)):
            time = time_list[i]
            price = int(price_list[i])
            if time <= 0 or price <= 0:
                continue
            # time = self._standardize_time(time)
            price_history[time] = price
        return price_history
