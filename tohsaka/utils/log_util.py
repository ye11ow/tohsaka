import logging
import os

LOG_FORMAT = '%(asctime)s %(levelname)s %(module)s(%(lineno)d) - %(message)s'
DATE_FORMAT = '%m/%d %H:%M:%S'

def set_file_logger(log):
    logging.basicConfig(filename=log, format=LOG_FORMAT, datefmt=DATE_FORMAT, level=logging.INFO)

def set_std_logger():
    logging.basicConfig(format=LOG_FORMAT, datefmt=DATE_FORMAT, level=logging.INFO)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.debug('start logging %s' % name)

    return logger