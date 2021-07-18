# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/18 18:22
# @Function:

from scrapy import Item, Field


class TweetItem(Item):
    """
    Tweet Spider Items
    """
    tweet_info = Field()
