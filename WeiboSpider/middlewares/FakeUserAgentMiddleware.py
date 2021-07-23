# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/18 19:12
# @Function:

import os
from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class FakeUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, ua):
        super(UserAgentMiddleware, self).__init__()
        self.ua = ua

    @classmethod
    def from_crawler(cls, crawler):
        path = f'{os.path.dirname(os.path.dirname(__file__))}/resource/0.1.11.json'
        ua = UserAgent(path=path)
        s = cls(ua=ua)
        return s

    def process_request(self, request, spider):
        request.headers['User-agent'] = self.ua.random
        return None
