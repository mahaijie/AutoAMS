"""news app
"""
from django.conf.urls import url, include, patterns
from idcroom.views import *

urlpatterns = patterns('idcroom.views',
                       url(r'^admin/idcroom/add/',  'idcroom_add',name='idcroom_add'),
                       url(r'^admin/idcroom/update/(?P<id>\d+)/$',  'idcroom_update',name='idcroom_update'),
                       url(r'^admin/idcroom/list/',  'idcroom_list',name='idcroom_list'),
                       url(r'^admin/idcroom/del/(?P<id>\d+)/$', 'idcroom_del',name='idcroom_del'),

                       )