# -*- coding: utf-8 -*-
from IdcAMS import commons
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Idcroom
from django.contrib.auth.decorators import login_required
import json

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
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，带星号（*）表单不能为空！")
            return render(request,'idcroom/idcroom_add.html',mydict)


        if Idcroom.objects.filter(name=name):
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，此名称已存在！")
            return render(request,'idcroom/idcroom_add.html',mydict)



        idcroom = Idcroom(
            name = name,
            user = user,
            comment = comment,
        )
        idcroom.save()
        commons.mynotice(request,"add","success")
        return HttpResponseRedirect("/idcroom/list/")

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
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，带星号（*）表单不能为空！")
            return render(request,'idcroom/idcroom_update.html',mydict)


        if sqldata.name != name and len(Idcroom.objects.filter(name=name)) >= 1:
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，此名称已存在！")
            return render(request,'idcroom/idcroom_update.html',mydict)


        idcroom = Idcroom.objects.get(id = id)
        idcroom.name = name
        # idcroom.user = user 不更新操作员
        idcroom.comment = comment


        idcroom.save()
        commons.mynotice(request,"update","success")
        return HttpResponseRedirect("/idcroom/list/")

    return render(request,'idcroom/idcroom_update.html',mydict)

@login_required
@commons.permission_validate
def idcroom_del(request,id):
    id = int(id)
    data = Idcroom.objects.get(id=id)
    # 如果数据被其他字段引用，则不删除，弹出提示
    #json_data = json.dumps({'status':False,'info':'此数据有正在被其他字段引用！'})
    #return HttpResponse(json_data)

    data.delete()
    json_data = json.dumps({'status':True,'info':''})

    return HttpResponse(json_data)

@login_required
@commons.permission_validate
def idcroom_list(request):
    sqldata = Idcroom.objects.all()

    mydict = {
        'sqldata':sqldata,
        'mynotice':'',
        'nav_idcroom_list':'true',
    }
    mydict['mynotice'] = commons.mynotice(request)

    return render(request,'idcroom/idcroom_list.html',mydict)
