# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/18 23:50
# @Function:

class InitialMiddleware(object):
    def __init__(self, max_retry_times):
        self.max_retry_times = max_retry_times

    @classmethod
    def from_crawler(cls, crawler):
        retry_times = crawler.settings.get('MAX_RETRY_TIME')
        return cls(max_retry_times=retry_times)

    def process_request(self, request, spider):
        request.meta['max_retry_times'] = self.max_retry_times
        request.meta['retried_times'] = 0
        return None
