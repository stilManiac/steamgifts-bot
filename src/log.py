import logging
import sys

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(stream = sys.stdout,
                    filemode = "w",
                    format = Log_Format,
                    level = logging.INFO)


def get_logger(name):
    return logging.getLogger(name)
