# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import os
import re
import time
import json
import random
import logging
from fake_useragent import UserAgent
from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


# to add random user-agent for every request
# to add random proxy IP address for every request
class RandomUaAndProxyIpMiddleware(UserAgentMiddleware):
    def __init__(self, ua, ip_num, api):
        super(UserAgentMiddleware, self).__init__()
        self.ua = ua
        self.api = api
        self.ip_num = ip_num

    @classmethod
    def from_crawler(cls, crawler):
        api = crawler.settings.get('PROXY_API')  # api to get proxy ip address, usually an url
        ip_num = int(re.findall(r'count=\d+', api)[0][6:])  # number of the proxy ip getting from url
        s = cls(ua=UserAgent(), ip_num=ip_num, api=api)
        return s

    @staticmethod
    def get_proxy_ip(ip_num):
        rad_index = random.randint(1, ip_num)
        file_path_dir = os.path.join(os.path.dirname(os.getcwd() + os.path.sep + '..'), 'proxy_utils\\proxy\\')
        # print(file_path_dir)
        file_path = os.path.join(file_path_dir, f"{str(rad_index)}.temp")
        # print(file_path)
        with open(file_path, 'r') as file:
            for line in file:
                proxy_ip = line.split(':')
        proxy = f'https://{proxy_ip[0]}:{proxy_ip[1]}'
        return proxy

    def process_request(self, request, spider):
        request.headers['User-agent'] = self.ua.random
        proxy = RandomUaAndProxyIpMiddleware.get_proxy_ip(self.ip_num)
        request.meta['proxy'] = proxy


# to solve crawling failed
class RetryMiddleware(object):

    def __init__(self, ip_num, retry_time=3):
        # self.logger = logger
        self.retry_time = retry_time
        self.ua = UserAgent()
        self.__err_count = {}  # request error times
        self.ip_num = ip_num

    @classmethod
    def from_crawler(cls, crawler):
        api = crawler.settings.get('PROXY_API')
        ip_num = int(re.findall(r'count=\d+', api)[0][6:])
        s = cls(ip_num=ip_num)
        return s

    def process_response(self, request, response, spider):
        if response.status == 418:
            # receive http status code 418, resend this request
            url_hash = hash(request.url)
            # to count the recrawling times for each request
            if url_hash not in self.__err_count.keys():
                self.__err_count[url_hash] = 0
            else:
                self.__err_count[url_hash] += 1
            # to resend this request and change the ua and proxy ip
            if self.__err_count[url_hash] < self.retry_time:
                request.headers['User-agent'] = self.ua.random
                proxy = RandomUaAndProxyIpMiddleware.get_proxy_ip(self.ip_num)
                request.meta['proxy'] = proxy
                logging.log(msg=time.strftime("%Y-%m-%d %H:%M:%S [RetryMiddleware] ")
                            + spider.name + ": restart crawl url:" + response.url, level=logging.INFO)
                return request
            else:
                # raise error IgnoreRequest to drop this request
                logging.log(msg=time.strftime("%Y-%m-%d %H:%M:%S [RetryMiddleware] ")
                            + spider.name + ": drop request by maximum retry, url:" + response.url, level=logging.INFO)
                raise IgnoreRequest
        else:
            try:
                parse_json = json.loads(response.text)
                if parse_json['ok'] == 0:
                    # crawl empty json string
                    # drop this request
                    logging.log(msg=time.strftime("%Y-%m-%d %H:%M:%S [RetryMiddleware] ")
                                + spider.name + ": drop request by empty json, url:" + response.url, level=logging.INFO)
                    raise IgnoreRequest
                else:
                    # request.meta['parse_json'] = parse_json
                    return response
            except json.JSONDecodeError:
                # error when json string decoding, drop this request
                if "<!DOCTYPE html>" in response.text:
                    # crawled string is a html file
                    return response
                else:
                    logging.log(msg=time.strftime("%Y-%m-%d %H:%M:%S [RetryMiddleware] ")
                                + spider.name + ": drop request by json decoding error, url:"
                                + response.url, level=logging.INFO)
                    raise IgnoreRequest



