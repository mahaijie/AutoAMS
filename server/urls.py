"""news app
"""
from django.conf.urls import url, include, patterns
from idcroom.views import *

urlpatterns = patterns('server.views',

                       url(r'^admin/server/list/',  'server_list',name='server_list'),
                       url(r'^admin/server/update/(?P<id>\d+)/$',  'server_update',name='server_update'),
                       url(r'^admin/server/updatemore/',  'server_updatemore',name='server_updatemore'),

                       )