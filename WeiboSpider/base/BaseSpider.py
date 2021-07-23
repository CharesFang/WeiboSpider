# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/23 15:32
# @Function:

from abc import ABC
from scrapy import Spider
from WeiboSpider.items import ErrorItem


class BaseSpider(Spider, ABC):
    allowed_domains = ['m.weibo.cn', "weibo.com", "weibo.cn"]

    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)

    def parse_err(self, response):
        item = ErrorItem()
        item['uid'] = response.request.meta['uid']
        item['url'] = response.request.url
        yield item
