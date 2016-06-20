"""common app
"""
from django.conf.urls import url, include, patterns
from common.views import *

urlpatterns = patterns('common.views',

                       url(r'^index.html',  'index', name='index'),
                       url(r'^$',  'index', name='index'),
                       url(r'^NoAccess.html',  'noaccess', name='noaccess'),
                       url(r'^admin/common/my_upload_file',  'my_upload_file', name='my_upload_file'),
                       #url(r'^login/$',  'login', name='login'),
                       )