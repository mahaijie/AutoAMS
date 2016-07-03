# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from django.conf.urls import url, include, patterns
from server.views import *

urlpatterns = [
    url(r'^server/list/', server_list),
    url(r'^server/update/(?P<id>\d+)/$', server_update),
    url(r'^server/updatemore/', server_updatemore),
    url(r'^server/view/(?P<id>\d+)/$', server_view),
    url(r'^server/onekey/$', server_onekey),
]