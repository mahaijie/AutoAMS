# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from django.conf.urls import url, include, patterns
from idcroom.views import *

urlpatterns = patterns('server.views',

                       url(r'^server/list/',  'server_list',name='server_list'),
                       url(r'^server/update/(?P<id>\d+)/$',  'server_update',name='server_update'),
                       url(r'^server/updatemore/',  'server_updatemore',name='server_updatemore'),
                       url(r'^server/view/(?P<id>\d+)/$',  'server_view',name='server_view'),

                       )