# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/18 18:20
# @Function:

from scrapy import Item, Field


class UserInfoItem(Item):
    """
    User Info Spider Item
    """
    user_info = Field()
