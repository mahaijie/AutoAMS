"""news app
"""
from django.conf.urls import url, include, patterns
from idcroom.views import *

urlpatterns = patterns('network.views',

                       url(r'^network/switch/list/',  'switch_list',name='switch_list'),
                       url(r'^network/switch/add/',  'switch_add',name='switch_add'),
                       url(r'^network/switch/update/(?P<id>\d+)/$',  'switch_update',name='switch_update'),
                       url(r'^network/switch/del/(?P<id>\d+)/$',  'switch_del',name='switch_del'),

                       )