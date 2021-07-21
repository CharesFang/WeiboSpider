# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/22 0:06
# @Function:

from scrapy import Item, Field


class LongtextItem(Item):
    longtext = Field()
    uid = Field()
    t_id = Field()
