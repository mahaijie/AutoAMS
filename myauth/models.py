# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from django.db import models
from django.contrib.auth.models import AbstractUser


class Group(models.Model):
    name = models.CharField('分组名称',default='',max_length=256)
    permissions = models.TextField('分组权限',default='')
    comment = models.TextField('分组备注',default='')

class User(AbstractUser):
    # 扩展中文名字
    name = models.CharField('姓名',default='',max_length=80)
    group = models.ForeignKey(Group,default=0,verbose_name='权限分组')
