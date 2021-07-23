# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/23 15:32
# @Function:

from scrapy import Spider


class BaseSpider(Spider):
    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)

    @staticmethod
    def parse_err(self, response):
        pass
