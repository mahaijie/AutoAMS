# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from django.conf.urls import url, include, patterns
from backup.views import *

urlpatterns = [
    url(r'^backup/serverbk/add/', serverbk_add),
    url(r'^backup/serverbk/addmore/', serverbk_addmore),
    url(r'^backup/serverbk/update/(?P<id>\d+)/$',  serverbk_update),
    url(r'^backup/serverbk/list/', serverbk_list),
    url(r'^backup/serverbk/del/(?P<id>\d+)/$', serverbk_del),

    url(r'^backup/diskbk/add/', diskbk_add),
    url(r'^backup/diskbk/addmore/', diskbk_addmore),
    url(r'^backup/diskbk/update/(?P<id>\d+)/$', diskbk_update),
    url(r'^backup/diskbk/list/', diskbk_list),
    url(r'^backup/diskbk/del/(?P<id>\d+)/$', diskbk_del),

    url(r'^backup/memorybk/add/', memorybk_add),
    url(r'^backup/memorybk/addmore/', memorybk_addmore),
    url(r'^backup/memorybk/update/(?P<id>\d+)/$', memorybk_update),
    url(r'^backup/memorybk/list/', memorybk_list),
    url(r'^backup/memorybk/del/(?P<id>\d+)/$', memorybk_del),
]