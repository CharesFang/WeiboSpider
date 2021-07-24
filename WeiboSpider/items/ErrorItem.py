# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/23 15:41
# @Function:

from scrapy import Item, Field


class ErrorItem(Item):
    uid = Field()
    url = Field()
