# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/18 19:13
# @Function:

from time import strftime
from logging import log, WARNING
from json import loads, JSONDecodeError
from scrapy.exceptions import IgnoreRequest


class RetryMiddleware(object):
    def __init__(self, max_retry_times):
        self.max_retry_times = max_retry_times

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        retry_times = settings.get('MAX_RETRY_TIME')
        return cls(max_retry_times=retry_times)

    def process_response(self, request, response, spider):
        """
            This function was designed to handle several mistakes occurred when crawling weibo pages.
            Firstly, the `process_response` function will check `retried_times` argument of every request obj in filed
            `meta`. If this request obj has been rescheduled over `max_retry_times`, the function will raise `Ignore-
            Request` to drop it.
            Secondly, the function will check response-obj's status code. If the code appears 418, 404 and any others,
            the function will resend this request to scrapy engine and add one to `retried_times` parameter. Otherwise,
            it will return response obj to pipelines.
            Finally, the function will parse crawled json string to a dict obj. If `ok` filed of the dict equals to `0`,
            it appears that spider crawled an empty page.
            Notably, if `JSONDecodeError` was triggered, it seems that there was something wrong with crawled pages. So,
            the function will resent the request.
        """
        retry_times = request.meta['retried_times'] + 1
        msg_template = f"{strftime('%Y-%m-%d %H:%M:%S [RetryMiddleware]')}, {spider.name}:"

        if self.max_retry_times < retry_times:
            msg = f"{msg_template} Drop request by maximum crawling times, target url: {request.url}."
            log(msg=msg, level=WARNING)
            raise IgnoreRequest
        else:
            if response.status in [418, 404]:
                msg = f"{msg_template} Return request obj due to http error code {response.status}, target url: {request.url}."
                log(msg=msg, level=WARNING)
                request.meta['retried_times'] += 1
                return request
            try:
                json_obj = loads(response.text)
                if json_obj['ok'] == 0:
                    msg = f"{msg_template} Crawled json string without data, target url: {request.url}."
                    log(msg=msg, level=WARNING)
                    request.meta['retried_times'] += 1
                    return request
                else:
                    return response
            except JSONDecodeError:
                msg = f"{msg_template} Json Decoding Error, target url: {request.url}."
                log(msg=msg, level=WARNING)
                raise IgnoreRequest
