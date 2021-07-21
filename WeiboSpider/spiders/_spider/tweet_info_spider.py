# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/16 16:59
# @Function:

import json
from scrapy import Spider, Request
from WeiboSpider.items import TweetItem
from WeiboSpider.config import TweetConfig


class TweetInfoSpider(Spider):
    name = "tweet_spider"
    allowed_domains = ['m.weibo.cn', 'weibo.com']

    def __init__(self, uid, *args, **kwargs):
        super(TweetInfoSpider, self).__init__(*args, **kwargs)
        self.__generator = TweetConfig()
        self.__uid_list = list(filter(None, uid.split('|')))

    def start_requests(self):
        pass

    def parse(self, response, **kwargs):
        pass

    def _parse_tweet(self, response, **kwargs):
        pass
