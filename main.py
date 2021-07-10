# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2020/6/21 0:58
# @Function: To start crawler

import os
import sys
from scrapy.cmdline import execute


if __name__ == '__main__':
    uid = "5619426492"
    # spider_cmd = "scrapy crawl HotSearchSpider"
    spider_cmd = f"scrapy crawl WeiboSpider -a uid={uid}"
    # spider_cmd = f"scrapy crawl FansListSpider -a uids=6511176063| -a fans_end=5 -a follows_end=5"
    # spider_cmd = 'scrapy crawl KeyWordsSpider -a keywords={"#赵露思#"} -a page_num=1'
    # spider_cmd = input("请输入运行命令:")
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(spider_cmd.split())

