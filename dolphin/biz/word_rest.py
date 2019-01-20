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
from dolphin.common.dolphinhttpclient import dolphinhttpclient

ssl._create_default_https_context = ssl._create_unverified_context

type = sys.getfilesystemencoding()

logger = logging.getLogger(__name__)

class WordRest:
    def __init__(self):
        return

    def get_query_key_word_by_restservice(self):
        url = confighelper.getGlobalValue(self, 'rest_service_address') + "/spider/api/v1/word"
        query_result = dolphinhttpclient.get_response_data(dolphinhttpclient,url)
        response = query_result["data"]
        return response

    def put_query_key_word_by_restservice(self,data):
        url = confighelper.getGlobalValue(self, 'rest_service_address') + "/spider/api/v1/word"
        query_result = dolphinhttpclient.put(dolphinhttpclient,url,data)
        response = query_result.data
        return response