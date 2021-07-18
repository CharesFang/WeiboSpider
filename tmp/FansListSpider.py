# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2020/5/7 16:34
# @Function: WeiboSystem of weibo user's follow and followers list


import json
import scrapy
from WeiboSpider.items import FansListItem, FollowsListItem


class FansListSpider(scrapy.Spider):
    name = 'FansListSpider'
    allowed_domains = ['m.weibo.cn', 'weibo.com']
    handle_httpstatus_list = [418]

    def __init__(self, uids, fans_end=10, follows_end=10, *args, **kwargs):
        super(FansListSpider, self).__init__(*args, **kwargs)
        self.uid_list = list(filter(None, uids.split('|')))
        self.root_url = 'https://m.weibo.cn/'
        self.api = {'common_api': 'api/container/getIndex?containerid=231051', 'fans_api_0': '_-_fans_-_',
                    'fans_api_1': '&since_id=', 'follows_api_0': '_-_followers_-_', 'follows_api_1': '&page='}
        self.page_range = {'fans': {'start': 1, 'end': int(fans_end)}, 'follows': {'start': 1, 'end': int(follows_end)}}

    def crawl_one(self, uid):
        fans_url_template = self.root_url + self.api['common_api'] + \
                            self.api['fans_api_0'] + uid + self.api['fans_api_1']
        follows_url_template = self.root_url + self.api['common_api'] + \
                               self.api['follows_api_0'] + uid + self.api['follows_api_1']
        fans_urls = [(fans_url_template + str(page_index)) for page_index in range(
            self.page_range['fans']['start'], self.page_range['fans']['end'] + 1)
        ]
        follows_url = [(follows_url_template + str(page_index)) for page_index in range(
            self.page_range['follows']['start'], self.page_range['follows']['end'] + 1
        )]
        return fans_urls, follows_url

    def start_requests(self):
        for uid in self.uid_list:
            fans_url, follows_url = self.crawl_one(uid)
            for url in fans_url:
                yield scrapy.Request(url=url, callback=self.parse_fans, meta={'__uid': uid})
            for url in follows_url:
                yield scrapy.Request(url=url, callback=self.parse_follows, meta={'__uid': uid})

    def parse_fans(self, response):
        cards = json.loads(response.text)['data']['cards']
        fans_item = FansListItem()
        fans_item['uid'] = response.meta['__uid']
        fans_list = []
        for crd in cards:
            if crd['card_type'] == 11:
                for card in crd['card_group']:
                    if card['card_type'] == 10:
                        fans_list.append(card['user'])
        fans_item['fans_list'] = fans_list
        yield fans_item

    def parse_follows(self, response):
        cards = json.loads(response.text)['data']['cards']
        follows_item = FollowsListItem()
        follows_item['uid'] = response.meta['__uid']
        follows_list = []
        for crd in cards:
            if crd['card_type'] == 11:
                for card in crd['card_group']:
                    if card['card_type'] == 10:
                        follows_list.append([card['user']])
        follows_item['follows_list'] = follows_list
        yield follows_item
