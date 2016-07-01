# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from django.conf.urls import url, include, patterns
from news.views import *

urlpatterns = [
    url(r'^news/column/add/', column_add),
    url(r'^news/column/update/(?P<id>\d+)/$',  column_update),
    url(r'^news/column/list/',  column_list),
    url(r'^news/column/del/(?P<id>\d+)/$', column_del),

    url(r'^news/article/add/',  article_add),
    url(r'^news/article/update/(?P<id>\d+)/$',  article_update),
    url(r'^news/article/del/(?P<id>\d+)/$', article_del),
    url(r'^news/article/list/', article_list),
    url(r'^news/article/view/(?P<id>\d+)/$',  article_view),
]