# -*- coding: utf-8 -*-
import scrapy
import json
import time
from dolphin.common.commonlogger import commonlogger
from dolphin.models.items import BookItem
from dolphin.biz.doubanspiderbizapirest import doubanspiderbizapirest
from dolphin.config.confighelper import confighelper

logger = commonlogger().getlogger()

class DoubanBookSpider(scrapy.Spider):
    name = 'doubanbook'
    allowed_domains = ['http://api.douban.com']
    start_urls = []

    def __init__(self):
        for index in range(1):
            random_book_id = doubanspiderbizapirest.get_douban_book_id_by_restservice(doubanspiderbizapirest)
            single_book_url = confighelper.getValue(self, 'global', 'douban_book_api_url') + str(random_book_id)
            self.start_urls.append(single_book_url)

    def parse(self, response):
        try:
            jsonresponse = json.loads(response.body_as_unicode())
            spider_man = confighelper.getGlobalValue(self,"spider_man")
            item = BookItem()
            publisher = []
            publisher.append(jsonresponse["publisher"])
            item["name"] = jsonresponse["title"]
            item["isbn"] = jsonresponse["isbn13"]
            item["publisher"] = publisher
            item["author"] = jsonresponse["author"]
            item["publish_year"] = jsonresponse["pubdate"]
            item["binding"] = jsonresponse["binding"]
            item["price"] = jsonresponse["price"]
            item["original_name"] = jsonresponse["origin_title"]
            item["translator"] = jsonresponse["translator"]
            item["pages"] = jsonresponse["pages"]
            item["creator"] = spider_man
            item["douban_id"] = jsonresponse["id"]
            yield item
        except Exception as e:
            logger.error(e)