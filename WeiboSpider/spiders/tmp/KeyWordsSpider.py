# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2020/5/8 20:51
# @Function: To crawl weibo information based on key words

import json
import scrapy
import logging
from time import time
from math import floor
from urllib.parse import quote
from .WeiboSpider import WeiboSpider
from ..items import KeyWordsItem


class KeyWordsSpider(WeiboSpider):
    # init parameters
    name = 'KeyWordsSpider'
    allowed_domains = ['m.weibo.cn', 'weibo.com']  # crawling sites
    handle_httpstatus_list = [418]  # http status code for not ignoring

    def __init__(self, keywords, page_num=5, *args, **kwargs):
        super(KeyWordsSpider, self).__init__(uid=None, *args, **kwargs)
        self.api = {
            'api_0': 'https://m.weibo.cn/api/container/getIndex?containerid=100103type',
            'api_1': '=61&q=',  # append keywords behind and url code this sentences
            'api_2': '&t=10&isnewpage=1&extparam=c_type=30&pos=2&mi_cid=100103&source=ranklist&flag=0&filter_type=realtimehot&cate=0',
            'api_3': '&display_time=',
            'api_4': '&luicode=10000011&lfid=231583&page_type=searchall&page=',
            'precise_time_api': 'https://m.weibo.cn/status/'
        }
        self.keywords_list = list(filter(None, keywords.split('|')))
        self.page_num = int(page_num)

    def start_requests(self):
        time_stamp = floor(time())
        for keywords in self.keywords_list:
            keywords_part = quote(self.api['api_1'] + keywords, encoding='utf-8')
            url_template = self.api['api_0'] + keywords_part + self.api['api_2'] + \
                           self.api['api_3'] + str(time_stamp) + self.api['api_4']
            for i in range(1, self.page_num + 1):
                url = url_template + str(i)
                yield scrapy.Request(url=url, callback=self.parse, meta={'key_words': keywords})

    def parse(self, response):
        data = json.loads(response.text)['data']
        cards = data['cards']
        for card in cards:
            if card['card_type'] == 9:
                item = KeyWordsItem()
                item['key_words'] = response.meta['key_words']
                item['is_crawled'] = False
                item['post'] = card['mblog']
                post_id = card['mblog']['id']
                precise_time_url = self.api['precise_time_api'] + post_id
                yield scrapy.Request(url=precise_time_url, callback=self.parse_precise_time, meta={'post_item': item})

    def parse_precise_time(self, response):
        # parse for precise time
        try:
            user_post_item = response.meta['post_item']
            precise_time = self.get_precise_time(response.text)
            user_post_item['post']['precise_time'] = precise_time
            yield user_post_item
        except Exception as e:
            self.logger.info(message="[key_words_spider] parse_precise_time error!" + repr(e), level=logging.ERROR)

