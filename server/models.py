# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from __future__ import unicode_literals

from django.db import models
from collections import OrderedDict
from idcroom.models import Idcroom


# 服务器资产表
class Server(models.Model):

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
    cpu = models.TextField('CPU',default='') # json格式存储
    memory = models.TextField('内存',default='') # json格式存储
    disk = models.TextField('硬盘',default='') # json格式存储
    network = models.TextField('网卡',default='') # json格式存储

    ip = models.CharField('ip',default='',max_length=256)
    manage_ip = models.CharField('管理ip',default='',max_length=256)
    all_ip = models.CharField('全部ip',default='',max_length=256)
    system = models.CharField('系统',default='',max_length=256)
    hostname = models.CharField('HOSTNAME',default='',max_length=256)
    idcroom = models.ForeignKey(Idcroom,default=0,verbose_name='所在机房')
    position = models.CharField('位置',default='',max_length=256) # json格式存储
    user = models.CharField('操作员',default='',max_length=256)
    status = models.CharField('状态',max_length=10,default='product') # 服务器状态,默认生产

    # 手动添加部分
    company = models.CharField('公司',default='',max_length=256)
    department = models.CharField('部门',default='',max_length=256)
    principal = models.CharField('负责人',default='',max_length=256)
    servicetype = models.CharField('服务类型',default='',max_length=256)
    comment = models.TextField('备注',default='')
    guarantee = models.CharField('保修年限',default='',max_length=256)
    buydate = models.CharField('购买日期',default='',max_length=256)
    uptime = models.DateTimeField('更新时间',auto_now=True,null=True)


