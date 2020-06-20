# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2020/6/21 0:38
# @Function: 

import pymongo


class DBConnector:
    def __init__(self):
        self.mongo_uri = "106.15.204.41:27017"
        self.mongo_database = "weibo"
        self.mongo_user_name = 'admin'
        self.mongo_pass_wd = "19981105"

    def create_mongo_connection(self):
        client = pymongo.MongoClient(self.mongo_uri)
        database = client[self.mongo_database]
        database.authenticate(self.mongo_user_name, self.mongo_pass_wd)
        return database, client
