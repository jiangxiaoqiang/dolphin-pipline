# -*- coding: UTF-8 -*-

import sys
import time
import threading
from dolphin.biz.doubanspiderbiz import doubanspiderbiz
from dolphin.biz.doubanspiderbizapi import doubanspiderbizapi
from dolphin.biz.doubanspiderbizapirest import doubanspiderbizapirest
from dolphin.common.commonlogger import commonlogger
from dolphin.config.confighelper import confighelper

commonloggerinstance = commonlogger()
logger = commonloggerinstance.getlogger()

# Pull data by web page
class doubanspider(threading.Thread):
    def __init__(self, who):
        super().__init__()
        self.name = who

    def run(self):
        while True:
            spiderbiz = doubanspiderbiz()
            spiderbiz.save_book_lists()
            time.sleep(5)

    def start_api_spider(self, threadName):
        while True:
            spiderbizapi = doubanspiderbizapi()
            spiderbizapi.save_book_lists()
            time.sleep(5)

# Invoke douban api to pull info from server client
# Direct connection with database
class apidoubanspider(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            try:
                spiderbizapi = doubanspiderbizapi()
                spiderbizapi.save_api_book_lists()
                time.sleep(18)
            except Exception as e:
                logger.error(e)

# Invoke rest api to pull info from client
# Communication with restful service
class restapidoubanspider(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            try:
                restspiderbizapi = doubanspiderbizapirest()
                restspiderbizapi.save_rest_api_book_lists()()
                time.sleep(8)
            except Exception as e:
                logger.error(e)

