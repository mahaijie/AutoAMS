# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from django.conf.urls import url, include, patterns
from idcroom.views import *

urlpatterns = [
    url(r'^idcroom/add/', idcroom_add),
    url(r'^idcroom/update/(?P<id>\d+)/$', idcroom_update),
    url(r'^idcroom/list/', idcroom_list),
    url(r'^idcroom/del/(?P<id>\d+)/$', idcroom_del),
]