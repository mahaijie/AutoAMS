# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from django.conf.urls import url, include, patterns

urlpatterns = patterns('backup.views',
                       url(r'^backup/serverbk/add/',  'serverbk_add',name='serverbk_add'),
                       url(r'^backup/serverbk/addmore/',  'serverbk_addmore',name='serverbk_addmore'),
                       url(r'^backup/serverbk/update/(?P<id>\d+)/$',  'serverbk_update',name='serverbk_update'),
                       url(r'^backup/serverbk/list/',  'serverbk_list',name='serverbk_list'),
                       url(r'^backup/serverbk/del/(?P<id>\d+)/$', 'serverbk_del',name='serverbk_del'),

                       url(r'^backup/diskbk/add/',  'diskbk_add',name='diskbk_add'),
                       url(r'^backup/diskbk/addmore/',  'diskbk_addmore',name='diskbk_addmore'),
                       url(r'^backup/diskbk/update/(?P<id>\d+)/$',  'diskbk_update',name='diskbk_update'),
                       url(r'^backup/diskbk/list/',  'diskbk_list',name='diskbk_list'),
                       url(r'^backup/diskbk/del/(?P<id>\d+)/$', 'diskbk_del',name='diskbk_del'),

                       url(r'^backup/memorybk/add/',  'memorybk_add',name='memorybk_add'),
                       url(r'^backup/memorybk/addmore/',  'memorybk_addmore',name='memorybk_addmore'),
                       url(r'^backup/memorybk/update/(?P<id>\d+)/$',  'memorybk_update',name='memorybk_update'),
                       url(r'^backup/memorybk/list/',  'memorybk_list',name='memorybk_list'),
                       url(r'^backup/memorybk/del/(?P<id>\d+)/$', 'memorybk_del',name='memorybk_del'),
                       )