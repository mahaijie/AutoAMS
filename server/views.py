# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from AutoAMS import commons
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Server
from django.contrib.auth.decorators import login_required

@login_required
@commons.permission_validate
def server_update(request,id):
    sqldata = Server.objects.get(id=id)

    mydict = {"sqldata":sqldata,
              "mynotice":"", # 状态提示条
              'status':Server.STATUS,
             }

    if request.method == 'POST':
        company = request.POST.get('company', '')
        department = request.POST.get('department', '')
        principal = request.POST.get('principal', '')
        servicetype = request.POST.get('servicetype', '')
        guarantee = request.POST.get('guarantee', '')
        buydate = request.POST.get('buydate', '')
        user = request.user.username # 操作员为当前登录用户，系统自动获取不允许手动修改
        status = request.POST.get('status','')
        comment = request.POST.get('comment', '')


        if company == '' or department == '' or principal == '' or servicetype == '' or guarantee == '' or buydate == '' :
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，带星号（*）表单不能为空！")
            return render(request,'server/server_update.html',mydict)


        server = Server.objects.get(id = id)
        server.company = company
        server.department = department
        server.principal = principal
        server.servicetype = servicetype
        server.guarantee = guarantee
        server.buydate = buydate
        server.user = user
        server.status = status
        server.comment = comment

        server.save()
        commons.mynotice(request,"update","success")
        return HttpResponseRedirect("/server/list/")

    return render(request,'server/server_update.html',mydict)

@login_required
@commons.permission_validate
def server_updatemore(request):

    mydict = {
        "mynotice":"", # 状态提示条
        'status':Server.STATUS,
        }

    if request.method == 'POST':
        moreid = request.GET.get('moreid', '')
        company = request.POST.get('company', '')
        department = request.POST.get('department', '')
        principal = request.POST.get('principal', '')
        servicetype = request.POST.get('servicetype', '')
        guarantee = request.POST.get('guarantee', '')
        buydate = request.POST.get('buydate', '')
        user = request.user.username # 操作员为当前登录用户，系统自动获取不允许手动修改
        status = request.POST.get('status','')
        comment = request.POST.get('comment', '')


        if company == '' or department == '' or principal == '' or servicetype == '' or guarantee == '' or buydate == '' :
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，带星号（*）表单不能为空！")
            return render(request,'server/server_updatemore.html',mydict)


        moreid = commons.str_to_list(moreid) #将传过来的字符串转换为list
        Server.objects.filter(id__in = moreid).update(company=company,department=department,principal=principal,servicetype=servicetype,guarantee=guarantee,buydate=buydate,user=user,status=status,comment=comment)
        commons.mynotice(request,"update","success")
        return HttpResponseRedirect("/server/list/")


    return render(request,'server/server_updatemore.html',mydict)

@login_required
@commons.permission_validate
def server_list(request):
    sqldata = Server.objects.all()

    mydict = {'sqldata':sqldata,
              'mynotice':'',
              'nav_server_list':"true",
              'status':Server.STATUS,
             }
    mydict['mynotice'] = commons.mynotice(request)

    return render(request,'server/server_list.html',mydict)

@login_required
@commons.permission_validate
def server_view(request,id):
    sqldata = Server.objects.get(id=id)

    mydict = {"sqldata":sqldata,
              "mynotice":"", # 状态提示条
              'status':Server.STATUS,
             }

    return render(request,'server/server_view.html',mydict)
