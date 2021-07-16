# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/14 13:42
# @Function: To Crawl Weibo User's information including user profile and tweets.

from _spider.user_info_spider import UserInfoSpider
from _spider.tweet_info_spider import TweetInfoSpider


class WeiboSpider(UserInfoSpider, TweetInfoSpider):
    def __init__(self):
        super(WeiboSpider, self).__init__()

    def start_requests(self):
        pass
