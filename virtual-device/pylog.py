# coding=utf-8

import logging
import logging.handlers

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR

def setLogger(logfile, level = INFO, fileSize = 102400, fileCount = 2, debug=True):
    """
    配置日志
    """
    logging.addLevelName(logging.ERROR, 'E')
    logging.addLevelName(logging.WARNING, 'W')
    logging.addLevelName(logging.INFO, 'I')
    logging.addLevelName(logging.DEBUG, 'D')

    logger = logging.getLogger()
    logger.setLevel(level)
    
    loghandler = logging.handlers.RotatingFileHandler(filename=logfile, maxBytes = fileSize, backupCount = fileCount)
    loghandler.setFormatter(logging.Formatter('%(asctime)s[%(levelname)s] %(message)s'))
    #loghandler.setLevel(level)
    logger.addHandler(loghandler)
    
    # add stderr log handler
    if debug:
        stdhandler = logging.StreamHandler()
        stdhandler.setFormatter(logging.Formatter('%(asctime)s[%(levelname)s] %(message)s'))
        logger.addHandler(stdhandler)

def getLogger():
    return logging.getLogger()

class Log:
    def __init__(self, name:str):
        self.name ="(" + name + ") "

    def e(self, msg, *args, **kwargs):
        logging.error(self.name + msg, *args, **kwargs)

    def w(self, msg, *args, **kwargs):
        logging.warning(self.name + msg, *args, **kwargs)

    def i(self, msg, *args, **kwargs):
        logging.info(self.name + msg, *args, **kwargs)

    def d(self, msg, *args, **kwargs):
        logging.debug(self.name + msg, *args, **kwargs)

    def getLogger(self):
        return logging.getLogger()

