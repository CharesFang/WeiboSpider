# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2020/4/26 16:05
# @Function: A crawler for Sina Weibo

import re
import json
import scrapy
import logging
from lxml import etree
from ..items import *


class WeiboSpider(scrapy.Spider):
    # init parameters
    name = 'WeiboSpider'
    allowed_domains = ['m.weibo.cn', 'weibo.com']  # crawling sites
    handle_httpstatus_list = [418]  # http status code for not ignoring

    def __init__(self, uid, *args, **kwargs):
        super(WeiboSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://m.weibo.cn/']
        self.uid = uid
        self.__user_info_api = {'api_0': 'api/container/getIndex?type=uid&value=', 'api_1': '&containerid=100505'}
        self.__weibo_info_api = {'api_0': 'api/container/getIndex?type=uid&value=',
                                 'api_1': '&containerid=107603', 'api_2': '&page=',
                                 'longtext_api': 'https://m.weibo.cn/statuses/extend?id=',
                                 'precise_time_api': 'https://m.weibo.cn/status/'}
        self.__weibo_page_range = 3

    def start_requests(self):
        # start of the crawler
        user_info_url = self.crawling_user_info()
        yield scrapy.Request(url=user_info_url, callback=self.parse_user, meta={'repeat_times': 0})
        weibo_info_urls = self.crawling_post_info()
        for weibo_info_url in weibo_info_urls:
            yield scrapy.Request(url=weibo_info_url, callback=self.parse_post)

    def crawling_user_info(self):
        # to generate user's profile information url
        user_info_url = self.start_urls[0] + self.__user_info_api['api_0'] + \
                        self.uid + self.__user_info_api['api_1'] + self.uid
        return user_info_url

    def crawling_post_info(self):
        # to generate user's tweet/post/weibo information url
        weibo_info_urls = []
        self.total_flag = 1
        for i in range(1, self.__weibo_page_range + 1):
            weibo_info_url = self.start_urls[0] + self.__weibo_info_api['api_0'] + self.uid + \
                             self.__weibo_info_api['api_1'] + self.uid + self.__weibo_info_api['api_2'] + str(i)
            weibo_info_urls.append(weibo_info_url)
        return weibo_info_urls

    def parse_user(self, response):
        # the parser for user profile
        user_info = json.loads(response.text)['data']['userInfo']
        del user_info['toolbar_menus']
        user_info_item = UserInfoItem()
        user_info_item['user_info'] = user_info
        yield user_info_item

    def parse_post(self, response):
        # the parser for user post
        weibo_info = json.loads(response.text)
        cardListInfo = weibo_info['data']['cardlistInfo']
        # crawl the total number of this user
        total_item = TotalNumItem()
        total_item['uid'] = self.uid
        total_item['total_num'] = cardListInfo['total']  # total number of user posts
        yield total_item
        # 有待完善，只需要做一个这样的就可以了
        for card in weibo_info['data']['cards']:
            if card['card_type'] == 9:
                # only card_type equals 9, we need
                mblog = card['mblog']
                user_post_item = UserPostItem()
                user_post_item['user_post'] = mblog
                if user_post_item['user_post']['isLongText']:
                    longtext_url = self.__weibo_info_api['longtext_api'] + mblog['id']
                    yield scrapy.Request(url=longtext_url, callback=self.parse_longtext,
                                         meta={'post_item': user_post_item})
                else:
                    precise_time_url = self.__weibo_info_api['precise_time_api'] + mblog['id']
                    yield scrapy.Request(url=precise_time_url, callback=self.parser_precise_time,
                                         meta={'post_item': user_post_item})

    def parse_longtext(self, response):
        # parser for longtext post
        user_post_item = response.meta['post_item']
        data = json.loads(response.text)['data']
        user_post_item['user_post']['Long_text'] = data['longTextContent']
        precise_time_url = self.__weibo_info_api['precise_time_api'] + user_post_item['user_post']['id']
        yield scrapy.Request(url=precise_time_url, callback=self.parser_precise_time,
                             meta={'post_item': user_post_item})

    def parser_precise_time(self, response):
        # parse for precise time
        try:
            page_text = etree.HTML(response.text)
            result = page_text.xpath('/html/body/script[1]/text()')
            time_str = re.findall(r'"created_at":.+"', "".join(result))
            user_post_item = response.meta['post_item']
            if time_str:
                precise_time = json.loads('{' + time_str[0] + '}')['created_at']
                user_post_item['user_post']['precise_time'] = precise_time
            else:
                user_post_item['user_post']['precise_time'] = None
            yield user_post_item
        except Exception as e:
            self.logger.info(message="[weibo_info_spider] parse_precise_time error!" + repr(e), level=logging.ERROR)





