# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/23 15:32
# @Function:

from abc import ABC
from scrapy import Spider
from WeiboSpider.items import ErrorItem


class BaseSpider(Spider, ABC):
    """
        Base Class for all spiders in this project. All the scrapy spiders must inherit this class and input the \
        parameter `uid`. `Uid` is a sting which contains several target user's id string and separated by `|`.

        This class also provides a static method named `get_uid_list which` receives the string `uid` and divides it
        into a list obj.

        The `parse_err` method is a general callback function to handle with the `IgnoreRequest` error.
    """

    allowed_domains = ['m.weibo.cn', "weibo.com", "weibo.cn"]

    def __init__(self, uid, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.uid = uid

    @staticmethod
    def get_uid_list(uid: str) -> list:
        return list(filter(None, uid.split('|')))

    def parse_err(self, response):
        item = ErrorItem()
        item['uid'] = response.request.meta['uid']
        item['url'] = response.request.url
        yield item
