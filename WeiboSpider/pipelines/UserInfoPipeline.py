# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/18 18:00
# @Function:

from WeiboSpider import DBConnector
from WeiboSpider.items import UserInfoItem


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
