# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2020/5/5 11:07
# @Function: To crawl the information of tht hot searches on Sina Weibo

import time
import json
import scrapy
from WeiboSpider.items import HotSearchItem
from math import floor


class HotSearchSpider(scrapy.Spider):
    name = 'HotSearchSpider'
    allowed_domains = ['m.weibo.cn', 'weibo.com']
    handle_httpstatus_list = [418]

    def __init__(self, *args, **kwargs):
        super(HotSearchSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://m.weibo.cn/']
        self.time_arg = floor(time.time())  # get time seconds as the essential arguments for crawling hot searches
        self.__target_url = f'https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26' \
                            f'disable_hot%3D1%26filter_type%3Drealtimehot&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C' \
                            f'&extparam=cate%3D10103%26pos%3D0_0%26mi_cid%3D100103%26filter_type%3Drealtimehot%' \
                            f'26c_type%3D30%26 display_time%3D{self.time_arg}&luicode=10000011&lfid=231583'

    def start_requests(self):
        url = self.__target_url
        yield scrapy.Request(url=url, callback=self.parse, meta={'repeat_times': 0})

    def parse(self, response):
        hot_search_item = HotSearchItem()
        hot_search_item['hot_search'] = json.loads(response.text)['data']['cards']
        hot_search_item['time_stamp'] = self.time_arg
        yield hot_search_item


