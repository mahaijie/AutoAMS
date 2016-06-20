# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Column, Article

class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'intro', 'nav_display', 'home_display')

class ArticleAdmin(admin.ModelAdmin):
    # 修改列表页显示方式
    list_display = ('title', 'slug', 'author', 'pub_date', 'update_time') # 排序
    search_fields = ('title','content') # 搜索条
    list_filter = ('title','author') # 过滤器
    date_hierarchy = 'pub_date' # 另外一种过滤日期的方式
    ording = ('pub_date',) # 可降序排序,测试了没发现效果


    # 修改添加编辑详情页显示方式
    fields = ('title', 'author', 'column', 'content', 'published') # 定义文章添加和修改也要编辑的字段及显示顺序
    # filter_horizontal=('column',) # 多对多字段选择显示样式修改,这里没用到多对多字段
    # raw_id_fields = ('author',) # 修改外键（ForeignKey）的显示方式

admin.site.register(Column, ColumnAdmin)
admin.site.register(Article, ArticleAdmin)
