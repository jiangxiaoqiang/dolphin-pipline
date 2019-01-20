# -*- coding: UTF-8 -*-
#encoding=utf-8

import sys
import json
import time
import urllib
import ssl
import string
import random
import logging
from bs4 import BeautifulSoup
from scrapy import Request
from dolphin.book import book
import requests
import unicodedata
from dolphin.common.commonlogger import commonlogger
import numpy as numpy
from dolphin.config.confighelper import confighelper
from dolphin.common.utils import utils
from dolphin.common.dolphinhttpclient import dolphinhttpclient

ssl._create_default_https_context = ssl._create_unverified_context

type = sys.getfilesystemencoding()

logger = logging.getLogger(__name__)

class SpiderUrlsRest:
    def __init__(self):
        return

    def get_query_url_by_restservice(self,spider_name):
        main_url = confighelper.getGlobalValue(self, 'rest_service_address') 
        param = "/spider/api/v1/spiderurls?spider_name=" + spider_name
        full_url = main_url + param
        query_result = dolphinhttpclient.get_response_data(dolphinhttpclient,full_url)
        response = query_result["data"]
        return response

    def put_query_url_by_restservice(self,data):
        response = {}
        try:
            url = confighelper.getGlobalValue(self, 'rest_service_address') + "/spider/api/v1/spiderurls"
            query_result = dolphinhttpclient.put(dolphinhttpclient,url,data)
            response = query_result["data"]
        except Exception as e:
            logger.error(e)
        return response