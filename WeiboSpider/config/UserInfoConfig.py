# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/17 1:23
# @Function:

from WeiboSpider.config.base import Config


class UserInfoConfig(Config):
    def __init__(self):
        super(UserInfoConfig, self).__init__()
        self.__api = {
            'api_0': 'api/container/getIndex?type=__uid&value=',
            'api_1': '&containerid=100505'
        }

    def __call__(self, uid):
        return self.gen_url(uid)

    def gen_url(self, uid: str):
        return self.url + self.__api['api_0'] + uid + self.__api['api_1'] + uid


if __name__ == '__main__':
    print(UserInfoConfig().gen_url('1157864602'))
