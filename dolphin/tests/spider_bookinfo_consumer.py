# --encoding:utf-8--

import logging
import urllib
import datetime
from scrapy.utils.serialize import ScrapyJSONDecoder
from kafka import KafkaConsumer

from dolphin.models.bookserializer import BookSerializer
from dolphin.serilizer.industry_identifiers_serializer import IndustryIdentifiersSerializer

logger = logging.getLogger(__name__)

class SpiderBookinfoConsumer:

    consumer = KafkaConsumer('dolphin-spider-google-book-bookinfo',
                         bootstrap_servers=['mq-server:9092'],
                         group_id = "google-book",
                         client_id = "dolphin-pipline-google-bookinfo-consumer-foolman",
                         # Manage kafka offsets manual
                         enable_auto_commit = False,
                         consumer_timeout_ms=15000)    

    def consume_bookinfo(self):
        while True:
            try:
                for books in self.consumer:
                    recv = "%s:%d:%d: key=%s value=%s" % (books.topic, books.partition, books.offset, books.key, books.value)
                    logger.info("Get books info: %s" ,recv)
                    self.parse_bookinfo(books.value)
                    #self.consumer.commit_async(callback=self.offset_commit_result)
            except Exception as e:
                logger.erorr(e)
    
    def offset_commit_result(self,offsets, response):
        print("offsets:" + offsets + ",response:" + response)

    def parse_bookinfo(self,bookinfos):
        str_body = str(bookinfos, encoding='utf-8')
        plan_json_text = urllib.parse.unquote_plus(str_body)
        _decoder = ScrapyJSONDecoder()
        standard_book_str = _decoder.decode(plan_json_text)
        self.save_single_book(standard_book_str)         

    def save_single_book(self,books):   
        dict_type = type(books)
        if(dict_type == str and len(books) < 5):
            logger.warn("Null book info")
            return
        if(books):
            for key in books:
                try:
                    single_book = books[key]
                    bookSerializer = BookSerializer(data = single_book) 
                    saved_book = bookSerializer.create(single_book)
                    industryIdentifiers = single_book["industry_identifiers"]          
                    self.save_identifiers_info(industryIdentifiers,saved_book.id)
                except Exception as e:
                    logger.error("save book encount an error,detail %s ,book info: %s",e,books[key])

    def save_identifiers_info(self,identifiers,book_id):
        if(identifiers):
            for identify in identifiers:        
                industryIdentifiersSerializer = IndustryIdentifiersSerializer(data = identify)
                identify["book_id"] = book_id
                is_valid = industryIdentifiersSerializer.is_valid()
                if(is_valid):
                    industryIdentifiersSerializer.save()



