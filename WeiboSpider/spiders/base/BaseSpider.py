# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/23 15:32
# @Function:

from scrapy import Spider
from WeiboSpider.items import ErrorItem


class BaseSpider(Spider):
    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)

    def parse_err(self, response):
        item = ErrorItem()
        item['uid'] = response.meta['uid']
        item['url'] = response.url
