from logger import setup_logging
from config_loader import get_config
import logging as logger
from constants import TYPE_TAG, URL_TAG
import os
import json
from parsers.parser_factory import ParserFactory

import sentry_sdk
sentry_sdk.init(
    "https://2decfad56249478cb20c17529c376ce5@o364523.ingest.sentry.io/5899794",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

setup_logging()
CUR_DIR = os.path.dirname(__file__)
DATA_OUTPUT_PATH = os.path.expanduser('~/git/vnfunds_data/data')
SYMBOL_OUTPUT_PATH = os.path.expanduser('~/git/vnfunds_data/data')

os.makedirs(DATA_OUTPUT_PATH, exist_ok=True)
os.makedirs(SYMBOL_OUTPUT_PATH, exist_ok=True)


def write_csv_data(name, data, type):
    out_filename = f"{CUR_DIR}/../data/{type}/{name}.csv"
    with open(out_filename, "w") as fo:
        fo.write("time,price\n")
        for time, price in data.items():
            fo.write(f'"{time}",{price}\n')
    logger.info(f"Saved data to {out_filename}")


def write_json_data(name, data, type):
    dir_path = f"{DATA_OUTPUT_PATH}/{type}"
    os.makedirs(dir_path, exist_ok=True)
    out_filename = f"{dir_path}/{name}.json"
    # convert dict data to json array
    json_data = []
    for key, value in data.items():
        json_data.append([key, value])
    with open(out_filename, "w") as fo:
        json.dump(json_data, fo, indent=4)
        # json.dump(json_data, fo)
    logger.info(f"Saved data to {out_filename}")


def create_list_symbols(config):
    filename = f"{SYMBOL_OUTPUT_PATH}/symbols.json"
    json_data = dict()
    for key, value in config.items():
        type = value[TYPE_TAG]
        if type not in json_data:
            json_data[type] = [key]
        else:
            json_data[type].append(key)
    with open(filename, "w") as fo:
        json.dump(json_data, fo, indent=4, sort_keys=True)
    logger.info(f"Created {filename}")


def main():
    config = get_config()
    for symbol, value in config.items():
        url = value[URL_TAG]
        type = value[TYPE_TAG]
        parser = ParserFactory.get_parser(symbol, type, url)
        try:
            price_history = parser.get_data()
            write_json_data(symbol, price_history, type)
        except Exception as e:
            logger.error(f"Cannot parse data for {symbol} from {url} . Error = {e}")
    create_list_symbols(config)
    logger.info("Done")


if __name__ == '__main__':
    main()
