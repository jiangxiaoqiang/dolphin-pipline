# --encoding:utf-8--

import urllib

from dolphin.common.spiderconst import SpiderConst
from dolphin.config.confighelper import confighelper
from dolphin.common.dolphinhttpclient import dolphinhttpclient


class GoogleBookBiz:
    def __init__(self):
        return

    def get_total_elements_num_by_keyword(self, initial_url):
        total_element = 0
        response_text = dolphinhttpclient.get_response_data_google(
            dolphinhttpclient, initial_url)
        if(response_text is not None):
            total_element = response_text["totalItems"]
        return total_element

    def get_scrapy_urls(self, query_key_word):        
        url_main = confighelper.getValue(self, 'global', 'google_book_api_url')
        initial_url = url_main + query_key_word    
        return initial_url
