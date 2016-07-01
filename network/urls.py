# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from django.conf.urls import url, include, patterns
from network.views import *

urlpatterns = [
    url(r'^network/switch/list/', switch_list),
    url(r'^network/switch/add/', switch_add),
    url(r'^network/switch/update/(?P<id>\d+)/$', switch_update),
    url(r'^network/switch/del/(?P<id>\d+)/$', switch_del),
    url(r'^network/switch/view/(?P<id>\d+)/$', switch_view),

    url(r'^network/switch_interface/getdata/(?P<id>\d+)/$', switch_interface_getdata),
]