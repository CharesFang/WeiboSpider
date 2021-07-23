# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/18 18:00
# @Function:

from WeiboSpider.items import UserInfoItem
from WeiboSpider.pipelines.base import Pipeline


class UserInfoPipeline(Pipeline):
    def __init__(self, db_connector):
        super(UserInfoPipeline, self).__init__(db_connector)

    def process_item(self, item, spider):
        if isinstance(item, UserInfoItem):
            self.db['user'].update_one({'uid': int(item['user_info']['id'])}, {'$set': item['user_info']}, upsert=True)
        return item
