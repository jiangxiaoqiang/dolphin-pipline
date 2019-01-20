# -*- coding: utf-8 -*-

import json
import logging
from dolphin.biz.doubanspiderbizapirest import doubanspiderbizapirest
from dolphin.common.commonlogger import commonlogger

logger = logging.getLogger(__name__)

class DoubanBookPipeline(object):
    def process_item(self, item, spider):
        try:
            str_items = json.dumps(dict(item))
            doubanspiderbizapirest.save_douban_book_by_restservice(doubanspiderbizapirest,str_items)
        except Exception as e:
            logger.error(e)
        return item

class AmazonBookPipeline(object):
    def process_item(self, item, spider):
        try:
            print("ddddd")        
        except Exception as e:
            logger.error(e)
        return item

class GoogleBookPipeline(object):
    def process_item(self, item, spider):         
        try:
            if(item):
                logger.info("saving books info...")
                doubanspiderbizapirest.save_douban_book_by_restservice(doubanspiderbizapirest,item)
            else:
                logger.warn("Spider's result is null...")
        except Exception as e:
            logger.error(e)
        return item