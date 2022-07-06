import functools
import configparser as cf
import logging
import datetime

config = cf.ConfigParser()
try:
    config.read('config.ini')
    cdef = config['DEF']
except KeyError as e:
    print("No config file detected! Add config file to .exe directory.")

if cdef['debug']:
    logging.basicConfig(filename=cdef['logfile'], level=logging.DEBUG, format="%(asctime)s %(message)s")
else:
    logging.basicConfig(filename=cdef['logfile'], level=logging.WARNING, format="%(asctime)s %(message)s")


def dec(func):
    def wrapper(*args, **kwargs):
        logging.debug("Started function {} with args {} at {}".format(func.__name__, args, datetime.datetime.now()))
        res = func(*args, **kwargs)
        logging.debug("Function {} resulted in {} at {}".format(func.__name__, res, datetime.datetime.now()))
        return res
    return wrapper

def dec_noargs(func):
    def wrapper(*args, **kwargs):
        logging.debug("Started function {} at {}".format(func.__name__, datetime.datetime.now()))
        res = func(*args, **kwargs)
        logging.debug("Function {} resulted in {} at {}".format(func.__name__, res, datetime.datetime.now()))
        return res
    return wrapper

