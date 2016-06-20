# -*- coding: utf-8 -*-
from django.shortcuts import render
from myauth.models import User,Group
from IdcAMS.settings import PERMISSIONS
import json,time,os,random

# status: 控制右上角提示框颜色，success添加成功(绿色)，warning为添加失败(橘黄色)，error红色
# content: 提示内容
def mynotice(status,info):
    if status !='' and info != '':
        return "toastr.%s('%s')"%(status,info)

# list转换为字符串（逗号间隔）
def list_to_str(list):
    if list:
        str = ",".join(list)
        return str
    else:
        return ""

# str(逗号间隔)转换为list
def str_to_list(str):
    if str:
        return str.split(',')
    else:
        return ""

# 装饰器函数（验证当前用户是否拥有view中的函数权限）
def permission_validate(func):
    def wrapper(request,*args, **kwargs):

        func_name = func.__name__ # 获取view中被装饰的函数名
        username = request.user.username
        user = User.objects.get(username = username)
        group = Group.objects.get(id = user.group_id)
        permissions = group.permissions

        permissions_list = str_to_list(permissions)
        if(func_name in permissions_list):
            return func(request,*args, **kwargs)
        else:
            return render(request,'common/NoAccess.html',{"info":PERMISSIONS[func_name]})

    return wrapper