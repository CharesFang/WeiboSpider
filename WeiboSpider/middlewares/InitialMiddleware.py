# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/18 23:50
# @Function:

class InitialMiddleware(object):

    def process_request(self, request, spider):
        if 'retried_times' not in request.meta.keys():
            request.meta['retried_times'] = 0
        return None
