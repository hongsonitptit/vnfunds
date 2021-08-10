import logging


def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format="[%(levelname)s] %(asctime)s <%(name)s> %(pathname)s:%(lineno)d: %(message)s")
