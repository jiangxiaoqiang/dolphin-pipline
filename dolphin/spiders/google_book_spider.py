# -*- coding: utf-8 -*-

import scrapy
import json
import time
import random
import logging
import urllib
from dolphin.models.items import BookItem
from dolphin.models.items import IndustryIdentifiersItem
from urllib.parse import urlencode, quote_plus
from dolphin.biz.google_book_biz import GoogleBookBiz
from dolphin.biz.word_rest import WordRest
from dolphin.biz.spider_urls_rest import SpiderUrlsRest
from dolphin.config.confighelper import confighelper

logger = logging.getLogger(__name__)

class GoogleBookSpider(scrapy.Spider):
    name = 'googlebook'
    #allowed_domains = ['googleapis.com','www.googleapis.com']
    query_key_word = ''
    word_entity = {}
    startIndex = 0    
    start_urls = [
    ]

    def __init__(self):
        try:
            """
                generate a random number for query google
                needs to build a key words collections
                it may build from user query dynamic
            """
            spider_name = "google-book-spider"
            self.word_entity = SpiderUrlsRest.get_query_url_by_restservice(self,spider_name)
            if(self.word_entity):
                self.query_key_word = self.word_entity[0]["scrapy_url"]
                scrapy_urls = GoogleBookBiz.get_scrapy_urls(GoogleBookBiz,self.query_key_word)
                self.start_urls.append(scrapy_urls)                    
        except Exception as e:
            logger.error(e)          

    def parse_total_item(self,book):
        books = {}
        if book["totalItems"] > 0:
            if(book.__contains__("items")):
                for item in book["items"]:
                    book = item["volumeInfo"]
                    single_book = self.parse_single_google_book(book, item)
                    if single_book is not None and len(single_book) > 0:
                        if item["id"] not in books.keys():
                            books[item["id"]] = single_book
        return books

    def parse_single_google_book(self, book, item):
        book_item = BookItem()
        publisher = []
        authors = []
        try:
            spider_man = confighelper.getGlobalValue(self, "spider_man")
            book_item["name"] = book["title"] 
            book_item["douban_id"] = item["id"]
            isbn = self.get_isbn(book,book_item)
            if(isbn is None):
                return None            
            if(book.__contains__("publisher")):
                publisher.append(book["publisher"])              
            else:
                publisher.append("Unknown")
            book_item["publisher"] = publisher
            if book.__contains__("authors"):
                authors.append(book["authors"])
                book_item["author"] = authors
            else:
                authors.append("佚名")
                book_item["author"] = authors
            if book.__contains__("publishedDate"):
                book_item["publish_year"] = book["publishedDate"]
            if(book.__contains__("pageCount")):            
                book_item["pages"] = book["pageCount"]
            book_item["creator"] = spider_man
            book_item["source"] = "Google Book"         
        except Exception as e:
            logger.error(e)
        return book_item

    def get_isbn(self, book,book_item):
        if book.__contains__("industryIdentifiers"):     
            industryIdentifiersItems = []     
            industryIdentifiers = book["industryIdentifiers"]
            if len(industryIdentifiers)>0:
                for item in industryIdentifiers:
                    industryIdentifiersItem = IndustryIdentifiersItem()
                    industryIdentifiersItem["type"] = item["type"]
                    industryIdentifiersItem["identifier"] = item["identifier"]
                    if (item["type"] == "ISBN_13"):
                        isbn13 = item["identifier"]
                        book_item["isbn"] = isbn13
                    if(item["type"] == "ISBN_10"):
                        isbn10 = item["identifier"]
                        book_item["isbn10"] = isbn10
                    industryIdentifiersItems.append(industryIdentifiersItem)
                book_item["industry_identifiers"] = industryIdentifiersItems
                return book_item
            else:
                return None
        else:
            return None

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, method='GET',callback=self.parse_httpbin,errback=self.errback_httpbin, dont_filter=True)

    def parse(self, response):       
        try:
            time.sleep(3)
            books = self.parse_recursive(response)
            yield books
        except Exception as e:
            logger.error(e)    

    def parse_httpbin(self, response):
        books = self.parse_recursive(response)
        yield books
        self.logger.info('Got successful response from {}'.format(response.url))
        # do something useful here...

    def errback_httpbin(self, failure):
        self.word_entity[0]["scrapy_status"] = -1
        SpiderUrlsRest.put_query_url_by_restservice(SpiderUrlsRest,self.word_entity[0])
        # log all failures
        self.logger.error(repr(failure))

    def parse_recursive(self,response):
        try:
            jsonresponse = json.loads(response.body_as_unicode())
            googleBookSpider = GoogleBookSpider()
            books = googleBookSpider.parse_total_item(jsonresponse)
            self.word_entity[0]["scrapy_status"] = 1
            SpiderUrlsRest.put_query_url_by_restservice(SpiderUrlsRest,self.word_entity[0])
            return books
        except Exception as e:
            self.word_entity[0]["scrapy_status"] = -1
            SpiderUrlsRest.put_query_url_by_restservice(SpiderUrlsRest,self.word_entity[0])
            logger.error(e)

