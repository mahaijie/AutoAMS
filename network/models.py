# -*- coding: utf-8 -*-
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
    sn = models.CharField('序列号',max_length=256)
    brand = models.CharField('品牌',max_length=256)
    model = models.CharField('型号',max_length=256)

    # 手动添加部分
    ip = models.CharField('ip',max_length=256)
    other_ip = models.CharField('其他ip',max_length=256)
    position = models.CharField('位置',max_length=256) # 机柜
    user = models.CharField('操作员',max_length=256)
    status = models.CharField('状态',max_length=10,default='product') # 状态,默认生产
    idcroom = models.ForeignKey(Idcroom,verbose_name='所在机房')
    snmpcommunity = models.CharField('snmp团体名',max_length=256)

    company = models.CharField('公司',max_length=256)
    department = models.CharField('部门',max_length=256)
    principal = models.CharField('负责人',max_length=256)
    comment = models.TextField('备注',default='')
    guarantee = models.CharField('保修年限',max_length=256)
    buydate = models.CharField('购买日期',max_length=256)
    uptime = models.DateTimeField('更新时间',auto_now=True,null=True)


