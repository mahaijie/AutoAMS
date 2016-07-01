# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from django.conf.urls import url, include, patterns
from common.views import *

urlpatterns = [
    url(r'^index.html', index),
    url(r'^$', index),
    url(r'^NoAccess.html', noaccess),
    url(r'^common/my_upload_file', my_upload_file),
]