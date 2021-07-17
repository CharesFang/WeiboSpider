# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/17 14:46
# @Function:

import pymongo


class DBConnector:
    def __init__(self):
        self.mongo_uri = "127.0.0.1"
        self.mongo_database = "weibo"
        self.mongo_user_name = "weibo"
        self.mongo_pass_wd = "123456"

    def connect(self):
        client = pymongo.MongoClient(self.mongo_uri)
        database = client[self.mongo_database]
        database.authenticate(self.mongo_user_name, self.mongo_pass_wd)
        return database, client
