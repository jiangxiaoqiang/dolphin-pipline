# -- encoding: utf-8 --

import logging
import configparser
import logging.handlers
import os
import time

config = configparser.ConfigParser()
configFilePath = os.path.abspath("dolphin/config.ini")
with open(configFilePath, "r", encoding="utf-8") as cfgfile:
    config.readfp(cfgfile)

class commonlogger:
    def __init__(self):
        now_date_time = time.strftime('%Y-%m-%d', time.localtime())
        logFileName = "./dolphin/log/spider" + now_date_time + ".log"
        handler = logging.handlers.RotatingFileHandler(logFileName, maxBytes=1024*1024*50, backupCount=2)
        format = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        formatter = logging.Formatter(format)
        handler.setFormatter(formatter)
        self.logger = logging.getLogger('tst')
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def getlogger(self):
        return self.logger
