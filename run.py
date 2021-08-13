# -*- coding: utf-8 -*-
# @Time    : 2021/8/13 13:40
# @Author  : CharesFang

from scrapy.cmdline import execute


if __name__ == '__main__':
    spider_cmd = "scrapy crawl weibo_spider -a uid=user0|user1"
    execute(spider_cmd.split())
