# -*- coding: utf-8 -*-
import scrapy
import json
import time
from scrapy.selector import Selector  

from dolphin.common.commonlogger import commonlogger
from dolphin.models.items import BookItem
from dolphin.biz.doubanspiderbizapirest import doubanspiderbizapirest
from dolphin.config.confighelper import confighelper

logger = commonlogger()

commonloggerinstance = commonlogger()
logger = commonloggerinstance.getlogger()

class DoubanBookSpider(scrapy.Spider):
    name = 'amazonbook'
    allowed_domains = ['https://www.amazon.cn']
    start_urls = ['https://www.amazon.cn/dp/B00QG9J4VU/ref=cngwdyfloorv2_recs_6?pf_rd_p=660d1d54-e365-44e8-8492-48f02a259225&pf_rd_s=desktop-2&pf_rd_t=36701&pf_rd_i=desktop&pf_rd_m=A1AJ19PSB66TGU&pf_rd_r=KFXFZK53S7Y0FGN1C8T8&pf_rd_r=KFXFZK53S7Y0FGN1C8T8&pf_rd_p=660d1d54-e365-44e8-8492-48f02a259225']

    def parse(self, response):
        try:
            item = BookItem()
            publisher = []
            sel = Selector(response)  
            sites = sel.xpath('//*[@id="detail_bullets_id"]/table/tr/td/div/ul/li')  
            print(sites)
            for site in sites:
                local_site = site.xpath('./text()')
                value1 =  site.xpath('./text()').extract() 
                value = site.xpath('./b/text()').extract()
                if '出版社:' == value: 
                    #link = site.xpath('a/@href').extract()  
                    print(value)
                    #item.publisher = value 
            
            yield item
        except Exception as e:
            logger.error(e)
