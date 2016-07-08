# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from __future__ import unicode_literals

from django.db import models
from idcroom.models import Idcroom
from collections import OrderedDict


class Serverbk(models.Model):
    sn = models.CharField('序列号',default='',max_length=255)
    brand = models.CharField('品牌',default='',max_length=255)
    model = models.CharField('型号',default='',max_length=255)
    cpu = models.TextField('CPU',default='') # json格式存储
    memory = models.TextField('内存',default='') # json格式存储
    disk = models.TextField('硬盘',default='') # json格式存储
    idcroom = models.ForeignKey(Idcroom,default='',verbose_name='所在机房')
    user = models.CharField('操作员',default='',max_length=255)
    comment = models.TextField('备注',default='')
    guarantee = models.CharField('保修年限',default='',max_length=255)
    buydate = models.CharField('购买日期',default='',max_length=255)
    uptime = models.DateTimeField('更新时间',auto_now=True,null=True)

class Diskbk(models.Model):
    # 状态，OrderedDict保持字典原来顺序
    STATUS = OrderedDict([
        ('backup','备件'),
        ('fault','故障'),
        ('scrap','报废'),
    ])
    sn = models.CharField('序列号',default='',max_length=255)
    brand = models.CharField('品牌',default='',max_length=255)
    type = models.CharField('类型',default='',max_length=255)
    capacity = models.CharField('容量',default='',max_length=255)
    status = models.CharField('状态',max_length=255,default='backup')
    idcroom = models.ForeignKey(Idcroom,default='',verbose_name='所在机房')
    user = models.CharField('操作员',default='',max_length=255)
    comment = models.TextField('备注',default='')
    guarantee = models.CharField('保修年限',default='',max_length=255)
    buydate = models.CharField('购买日期',default='',max_length=255)
    uptime = models.DateTimeField('更新时间',auto_now=True,null=True)

class Memorybk(models.Model):
    # 状态，OrderedDict保持字典原来顺序
    STATUS = OrderedDict([
        ('backup','备件'),
        ('fault','故障'),
        ('scrap','报废'),
    ])
    sn = models.CharField('序列号',default='',max_length=255)
    brand = models.CharField('品牌',default='',max_length=255)
    type = models.CharField('类型',default='',max_length=255)
    capacity = models.CharField('容量',default='',max_length=255)
    status = models.CharField('状态',max_length=255,default='backup')
    idcroom = models.ForeignKey(Idcroom,default='',verbose_name='所在机房')
    user = models.CharField('操作员',default='',max_length=255)
    comment = models.TextField('备注',default='')
    guarantee = models.CharField('保修年限',default='',max_length=255)
    buydate = models.CharField('购买日期',default='',max_length=255)
    uptime = models.DateTimeField('更新时间',auto_now=True,null=True)
