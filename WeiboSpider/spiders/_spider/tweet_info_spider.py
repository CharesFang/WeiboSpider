# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/16 16:59
# @Function:

from scrapy import Spider


class TweetInfoSpider(Spider):
    def __init__(self):
        super(TweetInfoSpider, self).__init__()

    def start_requests(self):
        pass

    def parse_tweet(self, response, **kwargs):
        pass
