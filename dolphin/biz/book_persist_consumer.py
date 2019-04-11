# -*- coding: UTF-8 -*-

import logging
import time
import urllib
import json
import ast
from dolphin.db.ssdb_client import SsdbClient
from scrapy.utils.serialize import ScrapyJSONDecoder
from dolphin.biz.doubanspiderbiz import doubanspiderbiz
from dolphin.models.bookserializer import BookSerializer
from dolphin.biz.spider_bookinfo_consumer import SpiderBookinfoConsumer

logger = logging.getLogger(__name__)

# Invoke rest api to pull info from client
# Communication with restful service
class BookPersistConsumer():
    def __init__(self):
        super().__init__()

    def run(self):
        try:
            spiderBookinfoConsumer = SpiderBookinfoConsumer()
            spiderBookinfoConsumer.consume_bookinfo()
        except Exception as e:
            logger.error("book persist failed,detail info %s",e)
        