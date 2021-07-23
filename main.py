# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2020/6/21 0:58
# @Function: To start crawler

import os
import sys
from scrapy.cmdline import execute


if __name__ == '__main__':
    spider_cmd = f"scrapy crawl user_info_spider -a uid=2142947104|"
    # spider_cmd = f"scrapy crawl tweet_spider -a uid=2142947104|"
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(spider_cmd.split())
