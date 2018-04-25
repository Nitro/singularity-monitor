import logging
import logging.handlers
import sys

LOG_FMT = '%(asctime)s %(levelname)8s [%(name)12s] %(message)s'


def get_logger(name):
    logging.basicConfig(format=LOG_FMT)
    handler = logging.StreamHandler(stream=sys.stdout)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.removeHandler(logger.handlers.pop())

    return logger
