# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from __future__ import unicode_literals

from django.db import models
from collections import OrderedDict
from idcroom.models import Idcroom


# 交换机资产表
class Switch(models.Model):

    # 状态，OrderedDict保持字典原来顺序
    STATUS = OrderedDict([
        ('product','生产'),
        ('test','测试'),
        ('fault','故障'),
        ('tackback','收回'),
        ('scrap','报废'),
    ])

    # 自动采集部分
    sn = models.CharField('序列号',default='',max_length=256)
    brand = models.CharField('品牌',default='',max_length=256)
    model = models.CharField('型号',default='',max_length=256)

    # 手动添加部分
    ip = models.CharField('ip',default='',max_length=256)
    other_ip = models.CharField('其他ip',default='',max_length=256)
    user = models.CharField('操作员',default='',max_length=256)
    status = models.CharField('状态',max_length=10,default='product') # 状态,默认生产
    idcroom = models.ForeignKey(Idcroom,default=0,verbose_name='所在机房')
    cabinet = models.CharField('机柜',default='',max_length=256)
    position = models.CharField('机位',default='',max_length=256)
    snmpcommunity = models.CharField('snmp团体名',default='',max_length=256)

    company = models.CharField('公司',default='',max_length=256)
    department = models.CharField('部门',default='',max_length=256)
    principal = models.CharField('负责人',default='',max_length=256)
    comment = models.TextField('备注',default='')
    guarantee = models.CharField('保修年限',default='',max_length=256)
    buydate = models.CharField('购买日期',default='',max_length=256)
    uptime = models.DateTimeField('更新时间',auto_now=True,null=True)

# 交换机接口表
class SwitchInterface(models.Model):
    name = models.CharField('接口名称',default='',max_length=256)
    cabinet = models.CharField('机柜',default='',max_length=256)
    position = models.CharField('机位',default='',max_length=256)
    user = models.CharField('操作员',default='',max_length=256)
    comment = models.TextField('备注',default='')
    uptime = models.DateTimeField('更新时间',auto_now=True,null=True)
    switch = models.ForeignKey(Switch,default=0,verbose_name='所属交换机')



