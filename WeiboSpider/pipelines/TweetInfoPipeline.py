# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/18 18:12
# @Function:

from WeiboSpider.items import TweetItem
from WeiboSpider.pipelines.base import Pipeline


class TweetInfoPipeline(Pipeline):
    def __init__(self, db_connector):
        super(TweetInfoPipeline, self).__init__(db_connector)

    def process_item(self, item, spider):
        if isinstance(item, TweetItem):
            self.db['tweet'].update_one({'id': item['tweet_info']['id']}, {'$set': item['tweet_info']}, upsert=True)
        return item
