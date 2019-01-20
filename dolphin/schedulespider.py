# -*- coding: UTF-8 -*-

import sys
import time
import os
import sched
import logging
#import ptvsd
from scrapy import cmdline
#from Scrapy.cmdline import execute
logger = logging.getLogger(__name__)

schedule = sched.scheduler ( time.time, time.sleep )

#ptvsd.enable_attach(address = ('10.142.0.2', 5678))
#ptvsd.wait_for_attach()

def period_execute():
  try:
    name = 'googlebook'
    cmd = 'scrapy crawl {0}'.format(name)
    os.system(cmd)
    #cmdline.execute(cmd.split())  
    print("scrapy complete!!!!!")
  except Exception as e:
    logger.error(e)


def period_action(inc):
  schedule.enter(inc,0,period_action,(inc,))
  period_execute()

def schedule_define():
  schedule.enter(0,0,period_action,(3,))

if __name__ == '__main__':
    try:
      schedule_define()
      schedule.run()
    except ImportError as exc:
      logger.error(exc)

  



