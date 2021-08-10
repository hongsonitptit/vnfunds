import yaml
import os
from constants import URL_TAG, TYPE_TAG

CUR_DIR = os.path.dirname(__file__)


def get_config() -> dict:
    config_file = f"{CUR_DIR}/../config/sources.yaml"
    with open(config_file) as fi:
        data = yaml.load(fi, Loader=yaml.FullLoader)
    config = dict()
    for type, items in data.items():
        if items is None:
            continue
        for item in items:
            if item is None:
                continue
            for name, url in item.items():
                config[name] = {
                    URL_TAG: url,
                    TYPE_TAG: type
                }
    return config


# print(get_config())
