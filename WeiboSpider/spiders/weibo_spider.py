# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/14 13:42
# @Function: To Crawl Weibo User's information including user profile and tweets.

from scrapy import Request
from ._spider.user_info_spider import UserInfoSpider
from ._spider.tweet_info_spider import TweetInfoSpider


class WeiboSpider(UserInfoSpider, TweetInfoSpider):
    """
        `Weibo_spider` is a wrapper of combination for both UserInfoSpider and TweetInfoSpider to crawl target user's \
        profile and tweets.
    """

    name = "weibo_spider"

    def __init__(self, uid, *args, **kwargs):
        super(WeiboSpider, self).__init__(uid, *args, **kwargs)

    def start_requests(self):
        uid_list = self.get_uid_list(self.uid)
        for uid in uid_list:
            u_url = self._u_generator.gen_url(uid)
            yield Request(
                url=u_url, dont_filter=True, meta={'uid': uid}, callback=self._parse_profile, errback=self.parse_err
            )
            t_url = self._t_generator.gen_url(uid=uid, page=None)
            yield Request(
                url=t_url, dont_filter=True, meta={'uid': uid}, callback=self._parse_tweet, errback=self.parse_err
            )

    def parse(self, response, **kwargs):
        pass
