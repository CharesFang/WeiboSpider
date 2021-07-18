# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/16 16:58
# @Function:

import json
from scrapy import Spider, Request
from WeiboSpider.items import UserInfoItem
from WeiboSpider.config import UserInfoConfig


class UserInfoSpider(Spider):
    name = "user_info_spider"
    allowed_domains = ['m.weibo.cn', "weibo.com", "weibo.cn"]

    def __init__(self, uid: str, *args, **kwargs):
        """"
            The user_info_spider will get target uids
            from cmd line argument 'uid' and each uid
            was separated by a vertical line '|'.
        """
        super(UserInfoSpider, self).__init__(*args, **kwargs)
        self.__generator = UserInfoConfig()
        self.uid_list = uid.split('|')

    def start_requests(self):
        """ Generate Request objs by target uid and target url generator """
        for uid in self.uid_list:
            url = self.__generator(uid)
            yield Request(url=url)

    def parse(self, response, **kwargs):
        print(response.request.meta)
        yield self._parse_profile(response)

    def _parse_profile(self, response):
        item = UserInfoItem()
        user_info = json.loads(response.text)['data']['userInfo']
        item['user_info'] = user_info
        return item
