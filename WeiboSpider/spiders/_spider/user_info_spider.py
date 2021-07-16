# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/16 16:58
# @Function:

from scrapy import Spider


class UserInfoSpider(Spider):
    def __init__(self):
        super(UserInfoSpider, self).__init__()

    def start_requests(self):
        pass

    def parse_profile(self, response, **kwargs):
        pass
