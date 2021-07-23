# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/22 0:51
# @Function:

from WeiboSpider.base import Pipeline
from WeiboSpider.items import LongtextItem


class LongtextPipeline(Pipeline):
    def __init__(self, *args, **kwargs):
        super(LongtextPipeline, self).__init__(*args, **kwargs)

    def process_item(self, item, spider):
        if isinstance(item, LongtextItem):
            self.db['longtext'].update_one({'id': item['t_id']}, {'$set': dict(item)}, upsert=True)
        return item
