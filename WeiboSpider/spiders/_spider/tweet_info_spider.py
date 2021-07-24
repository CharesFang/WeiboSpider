# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/16 16:59
# @Function:

from json import loads
from scrapy import Request
from WeiboSpider.base import BaseSpider
from WeiboSpider.config import TweetConfig
from WeiboSpider.items import TweetItem, LongtextItem


class TweetInfoSpider(BaseSpider):
    name = "tweet_spider"

    def __init__(self, uid, *args, **kwargs):
        """
            The `tweet_spider` was designed to crawl user's tweets.
            It firstly inherits the `BaseSpider` class, and implements `_parse_tweet` and `_parse_longtext` function to
            extract user's tweets or longtext respectively.
        """
        super(TweetInfoSpider, self).__init__(uid, *args, **kwargs)
        self._t_generator = TweetConfig()

    def start_requests(self):
        """
        generate crawling Request from designated uid.
        :return: Target Request obj.
        """
        uid_list = self.get_uid_list(self.uid)
        for uid in uid_list:
            url = self._t_generator.gen_url(uid=uid, page=None)
            yield Request(url=url, dont_filter=True, callback=self._parse_tweet, errback=self.parse_err,
                          meta={'uid': uid, 'last_page': 0})

    def _parse_tweet(self, response, **kwargs):
        """
            Parse crawled json str and tweet_spider iteratively generate new Request obj.
        """

        weibo_info = loads(response.text)
        data = weibo_info['data']
        page = data['cardlistInfo']['page']
        uid = response.meta['uid']
        last_page = response.meta['last_page']

        if page is not None and int(page) != last_page:
            url = self._t_generator.gen_url(uid=uid, page=page)
            yield Request(url=url, dont_filter=True, callback=self._parse_tweet, errback=self.parse_err,
                          meta={'uid': uid, 'last_page': int(page)})

        for card in data['cards']:
            item = TweetItem()
            card['mblog']['uid'] = uid
            item['tweet_info'] = card['mblog']
            if card['mblog']['isLongText']:
                t_id = card['mblog']['id']
                url = self._t_generator.gen_url(t_id=t_id)
                longtext_req = Request(
                    url=url, dont_filter=True, errback=self.parse_err,
                    callback=self._parse_longtext, meta={'uid': uid, 't_id': t_id}
                )
                yield longtext_req
            yield item

    def _parse_longtext(self, response, **kwargs):
        long_text = loads(response.text)
        item = LongtextItem()
        item['uid'] = response.meta['uid']
        item['t_id'] = response.meta['t_id']
        item['longtext'] = long_text['data']['longTextContent']
        yield item

    def parse(self, response, **kwargs):
        """
            Compulsorily implemented due to abstract method.
        """
        pass
