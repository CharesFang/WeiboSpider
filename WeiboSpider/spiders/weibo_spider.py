# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/14 13:42
# @Function: To Crawl Weibo User's information including user profile and tweets.

from _spider.user_info_spider import UserInfoSpider
from _spider.tweet_info_spider import TweetInfoSpider
from WeiboSpider.items import UserInfoItem


class WeiboSpider(UserInfoSpider, TweetInfoSpider):
    name = "weibo_spider"

    def __init__(self, *args, **kwargs):
        super(WeiboSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        pass

    def parse(self, response, **kwargs):
        pass