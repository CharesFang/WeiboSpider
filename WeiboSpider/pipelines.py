# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
from WeiboSpider.items import *
from WeiboSpider.database.DBConnector import DBConnector
from scrapy.exceptions import DropItem


class UserInfoPipeline:
    def __init__(self, db_connector):
        self.connector = db_connector

    @classmethod
    def from_crawler(cls, crawler):
        return cls(db_connector=DBConnector())

    def open_spider(self, spider):
        self.db, self.client = self.connector.connect()

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, UserInfoItem):
            self.db['user'].update({'uid': int(item['user_info']['id'])}, {'$set': item['user_info']}, upsert=True)
            return item
