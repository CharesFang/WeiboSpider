# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserInfoItem(scrapy.Item):
    # Item for user's profile information
    user_info = scrapy.Field()


class TotalNumItem(scrapy.Item):
    # Item for user's post num
    uid = scrapy.Field()
    total_num = scrapy.Field()


class UserPostItem(scrapy.Item):
    # Item for user's post content
    user_post = scrapy.Field()


class HotSearchItem(scrapy.Item):
    # Item for real time hot search information
    hot_search = scrapy.Field()
    time_stamp = scrapy.Field()


class FansListItem(scrapy.Item):
    uid = scrapy.Field()
    fans_list = scrapy.Field()


class FollowsListItem(scrapy.Item):
    uid = scrapy.Field()
    follows_list = scrapy.Field()


class KeyWordsItem(scrapy.Item):
    key_words = scrapy.Field()
    is_crawled = scrapy.Field()
    post = scrapy.Field()
