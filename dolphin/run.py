# -*- coding: utf-8 -*-
# @Time     : 2018/12/1 17:51
# @Author   : dolphin
 

from scrapy import cmdline

name = 'doubanbook'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())






