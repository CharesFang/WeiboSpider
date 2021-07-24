# -*- coding: utf-8 -*-
# @Author  : CharesFuns
# @Time    : 2021/7/18 17:59
# @Function:

from WeiboSpider.pipelines.ErrorPipeline import ErrorPipeline
from WeiboSpider.pipelines.UserInfoPipeline import UserInfoPipeline
from WeiboSpider.pipelines.LongtextPipeline import LongtextPipeline
from WeiboSpider.pipelines.TweetInfoPipeline import TweetInfoPipeline

__all__ = ['UserInfoPipeline', 'LongtextPipeline', 'ErrorPipeline', 'TweetInfoPipeline']
