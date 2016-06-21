# -*- coding: utf-8 -*-
from IdcAMS import commons
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Switch
from django.contrib.auth.decorators import login_required
from idcroom.models import Idcroom


@login_required
def switch_add(request):

    idcroom = Idcroom.objects.all() # 获取机房列表
    mydict = {
              "mynotice":"", # 状态提示条
              "status":Switch.STATUS,
              "idcroom":idcroom,
             }

    if request.method == 'POST':
        sn = request.POST.get('sn', '')
        ip = request.POST.get('ip', '')
        other_ip = request.POST.get('other_ip', '')
        snmpcommunity = request.POST.get('snmpcommunity', '')
        brand = request.POST.get('brand', '')
        model = request.POST.get('model', '')

        company = request.POST.get('company', '')
        department = request.POST.get('department', '')
        principal = request.POST.get('principal', '')
        idcroom_id = request.POST.get('idcroom_id', '')
        position = request.POST.get('position', '')
        guarantee = request.POST.get('guarantee', '')
        buydate = request.POST.get('buydate', '')
        user = request.user.username # 操作员为当前登录用户，系统自动获取不允许手动修改
        status = request.POST.get('status','')
        comment = request.POST.get('comment', '')


        if company == '' or department == '' or principal == '' or guarantee == '' or buydate == '' :
            mydict['mynotice'] = commons.mynotice("error","添加失败，带星号（*）表单不能为空！")
            return render(request,'network/switch_add.html',mydict)


        switch = Switch(
            sn = sn,
            ip = ip,
            other_ip = other_ip,
            snmpcommunity = snmpcommunity,
            brand = brand,
            model = model,
            company = company,
            department = department,
            principal = principal,
            idcroom_id = idcroom_id,
            position = position,
            guarantee = guarantee,
            buydate = buydate,
            user = user,
            status = status,
            comment = comment,
        )


        switch.save()

        return HttpResponseRedirect("/network/switch/list?action=add")

    return render(request,'network/switch_add.html',mydict)


@login_required
def switch_update(request,id):
    sqldata = Switch.objects.get(id=id)
    idcroom = Idcroom.objects.all() # 获取机房列表

    mydict = {"sqldata":sqldata,
              "mynotice":"", # 状态提示条
              'status':Switch.STATUS,
              "idcroom":idcroom,
             }

    if request.method == 'POST':
        sn = request.POST.get('sn', '')
        ip = request.POST.get('ip', '')
        other_ip = request.POST.get('other_ip', '')
        snmpcommunity = request.POST.get('snmpcommunity', '')
        brand = request.POST.get('brand', '')
        model = request.POST.get('model', '')

        company = request.POST.get('company', '')
        department = request.POST.get('department', '')
        principal = request.POST.get('principal', '')
        idcroom_id = request.POST.get('idcroom_id', '')
        position = request.POST.get('position', '')
        guarantee = request.POST.get('guarantee', '')
        buydate = request.POST.get('buydate', '')
        user = request.user.username # 操作员为当前登录用户，系统自动获取不允许手动修改
        status = request.POST.get('status','')
        comment = request.POST.get('comment', '')


        if company == '' or department == '' or principal == '' or guarantee == '' or buydate == '' :
            mydict['mynotice'] = commons.mynotice("error","更新失败，带星号（*）表单不能为空！")
            return render(request,'network/switch_update.html',mydict)


        switch = Switch.objects.get(id = id)
        switch.sn = sn
        switch.ip = ip
        switch.other_ip = other_ip
        switch.snmpcommunity = snmpcommunity
        switch.brand = brand
        switch.model = model
        switch.company = company
        switch.department = department
        switch.principal = principal
        switch.idcroom_id = idcroom_id
        switch.position = position
        switch.guarantee = guarantee
        switch.buydate = buydate
        switch.user = user
        switch.status = status
        switch.comment = comment

        switch.save()

        return HttpResponseRedirect("/network/switch/list?action=update")

    return render(request,'network/switch_update.html',mydict)

@login_required
def switch_list(request):
    sqldata = Switch.objects.all()

    mydict = {'sqldata':sqldata,
              'mynotice':'',
              'nav_switch_list':"true",
              'status':Switch.STATUS,
              'nav_network_switch_list':"true"
             }
    if request.method == 'GET':
        action = request.GET.get('action')
        if action == "update":
            mydict['mynotice'] = commons.mynotice("success","恭喜您，更新成功！")
        elif action == "add":
            mydict['mynotice'] = commons.mynotice("success","恭喜您，添加成功！")

    return render(request,'network/switch_list.html',mydict)
