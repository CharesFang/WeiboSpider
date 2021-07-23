# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/23 15:34
# @Function:

from WeiboSpider.base import Pipeline
from WeiboSpider.items import ErrorItem


class ErrorPipeline(Pipeline):
    def __init__(self, db_connector):
        super(ErrorPipeline, self).__init__(db_connector)

    def process_item(self, item, spider):
        if isinstance(item, ErrorItem):
            self.db['error_log'].update_one({'uid': item['uid']}, {'$set': dict(item)}, upsert=True)
            return item
