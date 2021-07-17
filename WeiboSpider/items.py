# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class UserInfoItem(Item):
    # Item for user's profile information
    user_info = Field()


class TotalNumItem(Item):
    # Item for user's post num
    uid = Field()
    total_num = Field()


class UserPostItem(Item):
    # Item for user's post content
    user_post = Field()


class HotSearchItem(Item):
    # Item for real time hot search information
    hot_search = Field()
    time_stamp = Field()


class FansListItem(Item):
    uid = Field()
    fans_list = Field()


class FollowsListItem(Item):
    uid = Field()
    follows_list = Field()


class KeyWordsItem(Item):
    key_words = Field()
    is_crawled = Field()
    post = Field()
