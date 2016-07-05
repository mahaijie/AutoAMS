# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from __future__ import unicode_literals

from django.db import models


class Idcroom(models.Model):
    name = models.CharField('机房名称',default='',max_length=255)
    user = models.CharField('操作员',default='',max_length=255)
    comment = models.TextField('备注',default='')


