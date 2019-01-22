# --encoding:utf-8--

import logging

from kafka import KafkaConsumer


class SpiderBookinfoConsumer:

    consumer = KafkaConsumer('dolphin-spider-google-book-bookinfo',
                         bootstrap_servers=['mq-server:9092'],
                         group_id = "google-book",
                         consumer_timeout_ms=5000)

    logger = logging.getLogger(__name__)

    def consume_bookinfo(self):
        while True:
            try:
                for msg in self.consumer:
                    recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
                    print(recv)
            except Exception as e:
                logger.erorr(e)





