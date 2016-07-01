# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from django.conf.urls import url, include, patterns
from DjangoUeditor import urls as DjangoUeditor_urls
from django.conf import settings

urlpatterns = [
    url(r'^ueditor/', include(DjangoUeditor_urls)),  # Ueditor
    url(r'^', include('common.urls')),  # common app urls(index,login,logout...)
    url(r'^', include('myauth.urls')),  # myauth app urls
    url(r'^', include('news.urls')),  # news app urls
    url(r'^', include('idcroom.urls')),  # idcroom app urls
    url(r'^', include('server.urls')),  # server app urls
    url(r'^', include('backup.urls')),  # backup app urls
    url(r'^', include('network.urls')),  # network app urls
]

# use Django server /media/ files
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )