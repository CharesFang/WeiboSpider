# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/17 1:23
# @Function:

from .base.Config import Config


class UserInfoConfig(Config):
    def __init__(self):
        super(UserInfoConfig, self).__init__()
        self.__api = {
            'api_0': 'api/container/getIndex?type=__uid&value=',
            'api_1': '&containerid=100505'
        }

    def gen_url(self, uid: str):
        return self.__url + self.__api['api_0'] + uid + self.__api['api_1'] + uid
