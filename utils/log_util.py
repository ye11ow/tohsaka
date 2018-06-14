import logging
import os

def get_logger(name):
    cwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    # logging.basicConfig(filename=os.path.join(cwd, name + '.log'), format='%(asctime)s %(levelname)s %(module)s(%(lineno)d) - %(message)s',
    #                     datefmt='%m/%d %H:%M:%S', level=logging.INFO)

    logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s(%(lineno)d) - %(message)s',
                        datefmt='%m/%d %H:%M:%S', level=logging.INFO)

    logger = logging.getLogger(name)
    logger.debug('start logging %s' % name)

    return logger