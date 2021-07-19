# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/18 23:50
# @Function:

class InitialMiddleware(object):

    def process_request(self, request, spider):
        request.meta['retried_times'] = 0
        return None
