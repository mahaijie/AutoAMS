# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from AutoAMS import commons
from AutoAMS.settings import PERMISSIONS #导入自定义权限字典
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import User,Group
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,HttpResponseRedirect
import json


@login_required
@commons.permission_validate
def group_add(request):
    mynotice = "" # 状态提示条
    mydict = {"mynotice": mynotice,
              "permissions_all":PERMISSIONS
             }

    if request.method == 'POST':
        name = request.POST.get('name', '')
        permissions = request.POST.getlist('permissions[]', '')
        comment = request.POST.get('comment', '')

        if name == '' or commons == '':
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，带星号（*）表单不能为空！")
            return render(request,'myauth/group_add.html',mydict)

        if Group.objects.filter(name=name):
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，此分组已存在！")
            return render(request,'myauth/group_add.html',mydict)


        group = Group(
            name = name,
            permissions = commons.list_to_str(permissions),
            comment = comment,
        )
        group.save()
        commons.mynotice(request,"add","success")
        return HttpResponseRedirect("/myauth/group/list?action=add")

    return render(request,'myauth/group_add.html',mydict)

@login_required
@commons.permission_validate
def group_update(request,id):

    #id = request.REQUEST.get('id')
    sqldata = Group.objects.get(id=id)
    permissions_list=commons.str_to_list(sqldata.permissions)

    # 根据键值和权限列表把列表格式化成字典
    permissions_sqldata = {}
    for value in permissions_list:
        permissions_sqldata[value] = PERMISSIONS[value]

    mynotice = "" # 状态提示条
    permissions = ""
    mydict = {"sqldata":sqldata,
              "mynotice":mynotice,
              "permissions_sqldata":permissions_sqldata,
              "permissions_all":PERMISSIONS,
             }

    if request.method == 'POST':
        name = request.POST.get('name', '')
        permissions = request.POST.getlist('permissions[]', '')
        comment = request.POST.get('comment', '')

        if name == '' or comment == '':
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，带星号（*）表单不能为空！")
            return render(request,'myauth/group_update.html',mydict)

        if sqldata.name != name and len(Group.objects.filter(name=name)) >= 1:
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，此分组已存在！")
            return render(request,'myauth/group_update.html',mydict)

        mydict["permissions"] = permissions
        group = Group.objects.get(id = id)
        group.name = name
        group.permissions = commons.list_to_str(permissions)
        group.comment = comment

        group.save()
        commons.mynotice(request,"update","success")
        return HttpResponseRedirect("/myauth/group/list?action=update")

    return render(request,'myauth/group_update.html',mydict)

@login_required
@commons.permission_validate
def group_del(request,id):
    id = int(id)
    data = Group.objects.get(id=id)
    # 如果数据被其他字段引用，则不删除，弹出提示
    #json_data = json.dumps({'status':False,'info':'此数据有正在被其他字段引用！'})
    #return HttpResponse(json_data)

    data.delete()
    json_data = json.dumps({'status':True,'info':''})

    return HttpResponse(json_data)

@login_required
@commons.permission_validate
def group_list(request):
    sqldata = Group.objects.all()

    mydict = {'sqldata':sqldata,
              'mynotice':'',
              'nav_myauth_group_list':"true",
              }
    mydict['mynotice'] = commons.mynotice(request)

    return render(request,'myauth/group_list.html',mydict)


@login_required
@commons.permission_validate
def user_add(request):

    mynotice = "" # 状态提示条
    groups = Group.objects.all() # 获取分组列表
    mydict = {"mynotice": mynotice,
              "groups": groups,
             }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        name = request.POST.get('name')
        email = request.POST.get('email', '')
        group_id = request.POST.get('group_id', '')
        is_active = request.POST.get('is_active','')

        if username == '' or name == '' or password == '':
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，带星号（*）表单不能为空！")
            return render(request,'myauth/user_add.html',mydict)

        if User.objects.filter(username=username):
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，此用户名已存在！")
            return render(request,'myauth/user_add.html',mydict)

        try:
            user = User(
                username = username,
                name = name,
                password = make_password(password, "pwd", 'pbkdf2_sha256'),
                email = email,
                group_id = group_id,
                is_active = is_active,
            )
            user.save()
            commons.mynotice(request,"add","success")
            return HttpResponseRedirect("/myauth/user/list/")
        except Exception:
            pass

    return render(request, 'myauth/user_add.html', {'groups':groups})

@login_required
@commons.permission_validate
def user_update(request,id):

    groups = Group.objects.all() # 获取分组列表
    sqldata = User.objects.get(id=id)

    mynotice = "" # 状态提示条
    mydict = {"mynotice": mynotice,
              "groups": groups,
			  "sqldata":sqldata,
             }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        name = request.POST.get('name')
        email = request.POST.get('email', '')
        group_id = request.POST.get('group_id', '')
        is_active = request.POST.get('is_active','')

        if username == '' or name == '' or password == '':
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，带星号（*）表单不能为空！")
            return render(request,'myauth/user_update.html',mydict)

        if sqldata.username != username and len(User.objects.filter(username=username)) >= 1:
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，此用户名已存在！")
            return render(request,'myauth/user_update.html',mydict)

        try:
            if sqldata.password != password:
                password = make_password(password, "pwd", 'pbkdf2_sha256')

            user = User.objects.get(id = id)
            #user.username = username #禁止用户修改username
            user.password = password
            user.name = name
            user.email = email
            user.group_id = group_id
            user.is_active = is_active

            user.save()
            commons.mynotice(request,"update","success")
            return HttpResponseRedirect("/myauth/user/list/")
        except Exception:
            pass

    return render(request, 'myauth/user_update.html',mydict)

def user_update_json(request,id):
    groups = Group.objects.all() # 获取分组列表
    sqldata = User.objects.get(id=id)

    json_data = json.dumps({'id':sqldata.id,
                            'username':sqldata.username,
                            'name':sqldata.name,
                            'password':sqldata.password,
                            'email':sqldata.email,
                            'group_id':sqldata.group_id,
                            'is_active':sqldata.is_active})

    return HttpResponse(json_data)

@login_required
@commons.permission_validate
def user_del(request,id):
    id = int(id)
    data = User.objects.get(id=id)
    # 如果数据被其他字段引用，则不删除，弹出提示
    #json_data = json.dumps({'status':False,'info':'此数据有正在被其他字段引用！'})
    #return HttpResponse(json_data)

    data.delete()
    json_data = json.dumps({'status':True,'info':''})

    return HttpResponse(json_data)

@login_required
@commons.permission_validate
def user_list(request):
    sqldata = User.objects.all()
    groups = Group.objects.all() # 获取分组列表

    groups_dict = {}
    for group in groups:
        groups_dict[group.id] = group.name

    mydict = {'sqldata':sqldata,
              'mynotice':'',
              'groups_dict':groups_dict,
              'nav_myauth_user_list':"true",
              }
    mydict['mynotice'] = commons.mynotice(request)

    return render(request,'myauth/user_list.html',mydict)

def check_user_username(request):
    username = request.GET.get("username")
    if (User.objects.filter(username=username)):
        result = "false"
    else:
        result = "true"
    return HttpResponse(result)

def check_user_username_update(request):
    id = request.GET.get("id")
    username = request.GET.get("username")
    sqldata = User.objects.get(id=id)
    if sqldata.username != username and len(User.objects.filter(username=username)) >= 1:
        result = "false"
    else:
        result = "true"
    return HttpResponse(result)

def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/index.html")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_page = request.GET.get('next')
        if next_page == None:
            next_page = "/index.html"

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next_page)
            else:
                return render(request, 'myauth/login.html', {'status':1,'info':"您的账户未激活，请联系管理员激活！"})
        else:
            return render(request, 'myauth/login.html', {'status':2,'info':"用户名或密码错误，请重试！"})

    return render(request, 'myauth/login.html',{'status':0})

login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login")
