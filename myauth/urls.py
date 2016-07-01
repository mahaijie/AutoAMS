# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from django.conf.urls import url, include, patterns
from myauth.views import *

urlpatterns = [
    url(r'^myauth/group/add/', group_add),
    url(r'^myauth/group/update/(?P<id>\d+)/$', group_update),
    url(r'^myauth/group/list/', group_list),
    url(r'^myauth/group/del/(?P<id>\d+)/$', group_del),

    url(r'^myauth/user/add/', user_add),
    url(r'^myauth/user/update/(?P<id>\d+)/$', user_update),
    url(r'^myauth/user/list/', user_list),
    url(r'^myauth/user/del/(?P<id>\d+)/$', user_del),

    url(r'^accounts/login', login_view),
    url(r'^accounts/logout', logout_view),

    url(r'^myauth/user/check_user_username/', check_user_username),
    url(r'^myauth/user/check_user_username_update/', check_user_username_update),
    url(r'^myauth/user/update_json/(?P<id>\d+)/$', user_update_json),
]