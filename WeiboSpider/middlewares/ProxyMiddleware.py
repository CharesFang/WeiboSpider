# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/18 19:13
# @Function:

import requests


class ProxyMiddleware(object):
    """
        According to the Scrapy docs, if every request's meta filed 'proxy' was set,
        the scrapy engine will ignore the build-in HttpProxyMiddleware.
        So, I disabled this middleware in settings.py.
    """

    def __init__(self, proxy_url):
        self.proxy_url = proxy_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.proxy_url)

    def get_random_proxy(self):
        resp = requests.get(self.proxy_url)
        return resp.text

    def process_request(self, request, crawler):
        proxy = self.get_random_proxy()
        request.meta['proxy'] = proxy
        return request
