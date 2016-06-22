# -*- coding: utf-8 -*-
from IdcAMS import commons
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Switch,SwitchInterface
from django.contrib.auth.decorators import login_required
from idcroom.models import Idcroom
import json,commands


@login_required
@commons.permission_validate
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


        if sn == '' or ip == '' or snmpcommunity == '':
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，带星号（*）表单不能为空！")
            return render(request,'network/switch_add.html',mydict)

        if Switch.objects.filter(sn=sn):
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，此序列号已存在！")
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
        commons.mynotice(request,"add","success")

        return HttpResponseRedirect("/network/switch/list/")

    return render(request,'network/switch_add.html',mydict)


@login_required
@commons.permission_validate
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


        if sn == '' or ip == '' or snmpcommunity == '':
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，带星号（*）表单不能为空！")
            return render(request,'network/switch_update.html',mydict)

        if sqldata.sn != sn and len(Switch.objects.filter(sn=sn)) >= 1:
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，此序列号已存在！")
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
        commons.mynotice(request,"update","success")
        return HttpResponseRedirect("/network/switch/list/")

    return render(request,'network/switch_update.html',mydict)

@login_required
@commons.permission_validate
def switch_list(request):
    sqldata = Switch.objects.all()

    mydict = {'sqldata':sqldata,
              'mynotice':'',
              'nav_switch_list':"true",
              'status':Switch.STATUS,
              'nav_network_switch_list':"true",
             }
    mydict['mynotice'] = commons.mynotice(request)


    return render(request,'network/switch_list.html',mydict)

@login_required
@commons.permission_validate
def switch_del(request,id):
    id = int(id)
    data = Switch.objects.get(id=id)
    # 如果数据被其他字段引用，则不删除，弹出提示
    #json_data = json.dumps({'status':False,'info':'此数据有正在被其他字段引用！'})
    #return HttpResponse(json_data)

    data.delete()
    json_data = json.dumps({'status':True,'info':''})

    return HttpResponse(json_data)

# 通过交换机snmp获取接口信息，并把获取的接口列表写入数据库
# snmpwalk -v2c -c public 10.168.1.1 .1.3.6.1.2.1.2.2.1.2 | awk '{print $4}'
def switch_interface_getdata(request,id):
    id = int(id)
    # 通过交换机id取得snmp团体名、IP
    sqldata = Switch.objects.get(id=id)
    snmpcommunity = sqldata.snmpcommunity
    ip = sqldata.ip
    oid = ".1.3.6.1.2.1.2.2.1.2"

    # 获取接口列表
    interfaces = commands.getstatusoutput("snmpwalk -v2c -c %s %s %s | awk '{print $4}'"%(snmpcommunity,ip,oid))
    if interfaces[0] != 0:
        return HttpResponse("error,%s"%(interfaces))

    interfaces = interfaces[1]
    interfaces = interfaces.split('\n')

    # 遍历接口列表，写入数据库

    n = 0
    for name in interfaces:
        switch_interface = SwitchInterface(
            name = name,
            switch_id = id,
        )
        switch_interface.save()
        n += 1
    return HttpResponse("成功插入%d个接口信息"%(n))