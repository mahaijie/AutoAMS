"""news app
"""
from django.conf.urls import url, include, patterns
from idcroom.views import *

urlpatterns = patterns('idcroom.views',
                       url(r'^idcroom/add/',  'idcroom_add',name='idcroom_add'),
                       url(r'^idcroom/update/(?P<id>\d+)/$',  'idcroom_update',name='idcroom_update'),
                       url(r'^idcroom/list/',  'idcroom_list',name='idcroom_list'),
                       url(r'^idcroom/del/(?P<id>\d+)/$', 'idcroom_del',name='idcroom_del'),

                       )