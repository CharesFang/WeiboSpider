# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/16 16:58
# @Function:

import json
from scrapy import Spider
from WeiboSpider.items import UserInfoItem
from ..config.UserInfoConfig import UserInfoConfig


class UserInfoSpider(Spider):
    def __init__(self):
        super(UserInfoSpider, self).__init__()
        self.__generator = UserInfoConfig()

    def start_requests(self):
        pass

    def parse_profile(self, response, **kwargs):
        pass
