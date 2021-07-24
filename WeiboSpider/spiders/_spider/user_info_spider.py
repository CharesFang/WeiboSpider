# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/16 16:58
# @Function:

import json
from scrapy import Request
from WeiboSpider.base import BaseSpider
from WeiboSpider.items import UserInfoItem
from WeiboSpider.config import UserInfoConfig


class UserInfoSpider(BaseSpider):
    """"
        The `user_info_spider` was designed to crawl user's profile information. The `_parse_profile` function was
        implemented to extract user's profile information.
    """

    name = "user_info_spider"

    def __init__(self, uid: str, *args, **kwargs):
        super(UserInfoSpider, self).__init__(uid, *args, **kwargs)
        self._u_generator = UserInfoConfig()

    def start_requests(self):
        """
            Generate Request objs by target uid and target url generator
        """
        uid_list = self.get_uid_list(self.uid)
        for uid in uid_list:
            url = self._u_generator(uid)
            yield Request(url=url, dont_filter=True, callback=self._parse_profile, errback=self.parse_err,
                          meta={'uid': uid})

    def _parse_profile(self, response):
        item = UserInfoItem()
        user_info = json.loads(response.text)['data']['userInfo']
        item['user_info'] = user_info
        yield item

    def parse(self, response, **kwargs):
        pass
