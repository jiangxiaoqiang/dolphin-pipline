# -*- coding: UTF-8 -*-
#encoding=utf-8

import sys
import time
import urllib
import logging
from bs4 import BeautifulSoup
import psycopg2
from dolphin.book import book
import requests
import unicodedata
from dolphin.common.commonlogger import commonlogger
import numpy as numpy
from dolphin.biz.doubanparser import doubanparser
from dolphin.config.confighelper import confighelper
from dolphin.common.utils import utils
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
logger = commonlogger()
type = sys.getfilesystemencoding()

logger = logging.getLogger(__name__)

class doubanspiderbiz:
    def __init__(self):
        return

    def get_single_book_detail_info(self,url, id):
        single_book = book()
        try:
            headers = utils.getHttpHeader()
            req = urllib.request.Request(
                url, headers=headers[numpy.random.randint(0, len(headers))])
            source_code = urllib.request.urlopen(req).read()
            plain_text = str(source_code,'utf-8')
            doubanparserinstance = doubanparser()
            single_book = doubanparserinstance.parseWebPage(plain_text)
        except Exception as e:
            logger.error(e)
        return single_book
