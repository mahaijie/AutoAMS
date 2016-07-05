# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from DjangoUeditor.models import UEditorField
from django.core.urlresolvers import reverse

class Column(models.Model):
    name = models.CharField('栏目名称',default='',max_length=255)
    slug = models.CharField('栏目网址',default='',max_length=255,db_index=True)
    intro = models.TextField('栏目简介',default='')

    nav_display = models.BooleanField('导航显示', default=False)
    home_display = models.BooleanField('首页显示', default=False)

class Article(models.Model):

    title = models.CharField('标题',default='',max_length=255)
    slug = models.CharField('网址',default='',max_length=255,db_index=True)
    #column = models.ManyToManyField(Column,verbose_name='归属栏目') # 多对多，一篇文章多个分类
    column = models.ForeignKey(Column,default='',verbose_name='分类')
    author = models.CharField('作者',default='',max_length=255)
    content = models.TextField('内容',default='',blank=True)
    count = models.IntegerField('统计',default='')
    pub_date = models.DateTimeField('发布时间',auto_now_add=True, editable=True)
    update_time = models.DateTimeField('更新时间',auto_now=True,null=True)
    published = models.BooleanField('正式发布',default=True)
