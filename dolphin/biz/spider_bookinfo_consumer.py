# --encoding:utf-8--

import logging
import urllib
import json
import time
import threading
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
                         consumer_timeout_ms=50000,
                         # consume from beginning
                         auto_offset_reset = "earliest",
                         max_poll_interval_ms =350000,
                         session_timeout_ms = 60000,
                         request_timeout_ms = 700000
                         )    

    def consume_bookinfo(self):
        while True:
            try:
                msg_pack = self.consumer.poll(timeout_ms=500,max_records=1)
                for messages in msg_pack.items():
                    for message in messages:
                        #for books in self.consumer.poll(max_records = 5):
                        logger.info("Get books info offset: %s" ,message.offset)                    
                        self.sub_process_handle(message.value,message.offset)                    
            except Exception as e:
                logger.error(e)
    
    def sub_process_handle(self,bookinfo,offset):     
        number_of_threadings = len(threading.enumerate())
        if(number_of_threadings < 13):
            t = threading.Thread(target=self.background_process,name="offset-" + str(offset), args=(bookinfo,), kwargs={})
            t.start()
        else:
            # If all threading running
            # Using main thread to handle
            # Slow down kafka consume speed
            logger.info("Reach max handle thread,sleep 20s to wait thread release...")
            time.sleep(20)            
            self.sub_process_handle(bookinfo,offset)

    def background_process(self,bookinfo):        
        self.parse_bookinfo(bookinfo)
        self.consumer.commit_async(callback=self.offset_commit_result)  

    def offset_commit_result(self,offsets, response):
        if(response is None):
            logger.info("commit offset success,offsets: %s",offsets)
        else:
            logger.error("commit offset failed,detail: %s",response)

    def parse_bookinfo(self,bookinfos):
        str_body = str(bookinfos, encoding='utf-8')
        plan_json_text = urllib.parse.unquote_plus(str_body)
        _decoder = ScrapyJSONDecoder()
        standard_book_str = _decoder.decode(plan_json_text)
        self.save_single_book(standard_book_str)         

    def save_single_book(self,books):   
        dict_type = type(books)
        if(dict_type == str and len(books) < 5):
            logger.debug("Null book info")
            return
        if(books):
            for key in books:
                try:
                    single_book = books[key]
                    bookSerializer = BookSerializer(data = single_book) 
                    saved_book = bookSerializer.create(single_book)
                    thread_name = threading.current_thread().name
                    logger.debug("thread " + thread_name + " saving book: %s ",single_book) 
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



