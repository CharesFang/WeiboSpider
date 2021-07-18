# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/18 19:00
# @Function:

from abc import abstractmethod, ABC
from WeiboSpider.database import DBConnector


class Pipeline(ABC):
    def __init__(self, db_connector):
        self.connector = db_connector

    @classmethod
    def from_crawler(cls, crawler):
        return cls(db_connector=DBConnector())

    def open_spider(self, spider):
        self.db, self.client = self.connector.connect()

    def close_spider(self, spider):
        self.client.close()

    @abstractmethod
    def process_item(self, item, spider):
        pass
