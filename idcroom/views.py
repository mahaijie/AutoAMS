# -*- coding: utf-8 -*-
from IdcAMS import commons
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Idcroom
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django import forms
from DjangoUeditor.forms import UEditorField
from django.contrib.auth.decorators import login_required

@login_required
@commons.permission_validate
def idcroom_add(request):


    mydict = {"mynotice": "", # 状态提示条
             }

    if request.method == 'POST':
        name = request.POST.get('name', '')
        user = request.user.username
        comment = request.POST.get('comment', '')

        if name == '' and comment == '':
            mydict['mynotice'] = commons.mynotice("error","添加失败，带星号（*）表单不能为空！")
            return render(request,'idcroom/idcroom_add.html',mydict)


        if Idcroom.objects.filter(name=name):
            mydict['mynotice'] = commons.mynotice("error","添加失败，此名称已存在！")
            return render(request,'idcroom/idcroom_add.html',mydict)



        idcroom = Idcroom(
            name = name,
            user = user,
            comment = comment,
        )
        idcroom.save()

        return HttpResponseRedirect("/admin/idcroom/list?action=add")

    return render(request,'idcroom/idcroom_add.html',mydict)

@login_required
@commons.permission_validate
def idcroom_update(request,id):

    #id = request.REQUEST.get('id')
    sqldata = Idcroom.objects.get(id=id)

    mydict = {"sqldata":sqldata,
              "mynotice":"", # 状态提示条
             }

    if request.method == 'POST':
        name = request.POST.get('name', '')
        user = request.POST.get('user', '')
        comment = request.POST.get('comment', '')


        if name == '' and comment == '':
            mydict['mynotice'] = commons.mynotice("error","更新失败，带星号（*）表单不能为空！")
            return render(request,'idcroom/idcroom_update.html',mydict)


        if sqldata.name != name and len(Idcroom.objects.filter(name=name)) >= 1:
            mydict["mynotice"] = commons.mynotice("error","更新失败，此名称已存在！")
            return render(request,'idcroom/idcroom_update.html',mydict)


        idcroom = Idcroom.objects.get(id = id)
        idcroom.name = name
        # idcroom.user = user 不更新操作员
        idcroom.comment = comment


        idcroom.save()

        return HttpResponseRedirect("/admin/idcroom/list?action=update")

    return render(request,'idcroom/idcroom_update.html',mydict)

@login_required
@commons.permission_validate
def idcroom_del(request,id):
    id = int(id)
    data = Idcroom.objects.get(id=id)
    data.delete()

    return HttpResponseRedirect("/admin/idcroom/list?action=del")

@login_required
@commons.permission_validate
def idcroom_list(request):
    sqldata = Idcroom.objects.all()

    mynotice = ""
    if request.method == 'GET':
        action = request.GET.get('action')
        if action == "add":
            mynotice = commons.mynotice("success","恭喜您，添加成功！")
        elif action == "update":
            mynotice = commons.mynotice("success","恭喜您，更新成功！")
        elif action == "del":
            mynotice = commons.mynotice("success","恭喜您，删除成功！")

    return render(request,'idcroom/idcroom_list.html',{'sqldata':sqldata,'mynotice':mynotice,'nav_idcroom_list':"true"})
