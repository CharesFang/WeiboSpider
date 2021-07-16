# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/17 1:09
# @Function:

from abc import ABC, abstractmethod


class Config(ABC):
    def __init__(self):
        self.__url = "https://m.weibo.cn/"

    @abstractmethod
    def gen_url(self, *args, **kwargs):
        pass
