# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Idcroom(models.Model):
    name = models.CharField('机房名称',max_length=256)
    user = models.CharField('操作员',max_length=256)
    comment = models.TextField('备注',default='')


