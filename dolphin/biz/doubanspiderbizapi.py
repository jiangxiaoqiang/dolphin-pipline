# -*- coding: UTF-8 -*-
#encoding=utf-8

import sys
import json
import time
import urllib
import ssl
import string
import random
import gzip
from bs4 import BeautifulSoup
from scrapy import Request
import psycopg2
from dolphin.book import book
import requests
import unicodedata
from dolphin.common.commonlogger import commonlogger
import numpy as numpy
from dolphin.biz.doubanparser import doubanparser
from dolphin.config.confighelper import confighelper
from dolphin.biz.doubanspiderbiz import doubanspiderbiz
from dolphin.common.utils import utils

ssl._create_default_https_context = ssl._create_unverified_context
logger = commonlogger()
type = sys.getfilesystemencoding()

commonloggerinstance = commonlogger()
logger = commonloggerinstance.getlogger()

class doubanspiderbizapi:
    def __init__(self):
        return

    def get_api_single_book_detail_info(self, url, id):
        single_book = book()
        try:
            headers = utils.getHttpHeader()
            #proxy_support = urllib.request.ProxyHandler({'https': 'localhost:8888'})
            #opener = urllib.request.build_opener(proxy_support)
            #urllib.request.install_opener(opener)
            req = urllib.request.Request(url)
            for key in headers:
                req.add_header(key, headers[key])
            source_code = urllib.request.urlopen(req).read()
            plain_text = gzip.GzipFile(fileobj=source_code)
            plain_text_decode = str(plain_text, 'utf-8')
            single_book = json.loads(plain_text_decode)
        except Exception as e:
            logger.error(e)
        return single_book
    
