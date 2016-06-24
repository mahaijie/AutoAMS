# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from IdcAMS import commons
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Serverbk,Diskbk,Memorybk
from idcroom.models import Idcroom
from django.contrib.auth.decorators import login_required
import json,time,xlrd  # 请使用pip install xlrd安装该模块
from collections import OrderedDict

# 服务器备件的增删改查，批量导入
@login_required
@commons.permission_validate
def serverbk_add(request):

    idcroom = Idcroom.objects.all() # 获取机房列表

    mydict = {"mynotice": "", # 状态提示条
              "idcroom":idcroom,
             }

    if request.method == 'POST':
        sn = request.POST.get('sn', '')
        brand = request.POST.get('brand', '')
        model = request.POST.get('model', '')
        cpu = request.POST.get('cpu', '')
        memory = request.POST.get('memory', '')
        disk = request.POST.get('disk', '')
        idcroom_id = request.POST.get('idcroom_id', '')
        user = request.user.username
        comment = request.POST.get('comment', '')
        guarantee = request.POST.get('guarantee', '')
        buydate = request.POST.get('buydate', '')


        if sn == '' or brand == '' or model == '' or cpu == '' or memory == '' or disk == '' or guarantee == '' or buydate == '':
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，带星号（*）表单不能为空！")
            return render(request,'backup/serverbk_add.html',mydict)


        if Serverbk.objects.filter(sn=sn):
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，此序列号已存在！")
            return render(request,'backup/serverbk_add.html',mydict)



        serverbk = Serverbk(
            sn = sn,
            brand = brand,
            model = model,
            cpu = cpu,
            memory = memory,
            disk = disk,
            idcroom_id = idcroom_id,
            user = user,
            comment = comment,
            guarantee = guarantee,
            buydate = buydate,
        )
        serverbk.save()
        commons.mynotice(request,"add","success")
        return HttpResponseRedirect("/backup/serverbk/list/")

    return render(request,'backup/serverbk_add.html',mydict)

@login_required
@commons.permission_validate
def serverbk_update(request,id):

    #id = request.REQUEST.get('id')
    sqldata = Serverbk.objects.get(id=id)
    idcroom = Idcroom.objects.all() # 获取机房列表

    mydict = {"sqldata":sqldata,
              "mynotice":"", # 状态提示条
              "idcroom":idcroom
             }

    if request.method == 'POST':
        sn = request.POST.get('sn', '')
        brand = request.POST.get('brand', '')
        model = request.POST.get('model', '')
        cpu = request.POST.get('cpu', '')
        memory = request.POST.get('memory', '')
        disk = request.POST.get('disk', '')
        idcroom_id = request.POST.get('idcroom_id', '')
        user = request.user.username
        comment = request.POST.get('comment', '')
        guarantee = request.POST.get('guarantee', '')
        buydate = request.POST.get('buydate', '')


        if sn == '' or brand == '' or model == '' or cpu == '' or memory == '' or disk == '' or guarantee == '' or buydate == '':
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，带星号（*）表单不能为空！")
            return render(request,'backup/serverbk_update.html',mydict)


        if sqldata.sn != sn and len(Idcroom.objects.filter(sn=sn)) >= 1:
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，此序列号已存在！")
            return render(request,'backup/serverbk_update.html',mydict)


        serverbk = Serverbk.objects.get(id = id)
        serverbk.sn = sn
        serverbk.brand = brand
        serverbk.model = model
        serverbk.cpu = cpu
        serverbk.memory = memory
        serverbk.disk = disk
        serverbk.idcroom_id = idcroom_id
        serverbk.user = user
        serverbk.comment = comment
        serverbk.guarantee = guarantee
        serverbk.buydate = buydate

        serverbk.save()
        commons.mynotice(request,"update","success")
        return HttpResponseRedirect("/backup/serverbk/list/")

    return render(request,'backup/serverbk_update.html',mydict)

@login_required
@commons.permission_validate
def serverbk_del(request,id):
    id = int(id)
    data = Serverbk.objects.get(id=id)
    # 如果数据被其他字段引用，则不删除，弹出提示
    #json_data = json.dumps({'status':False,'info':'此数据有正在被其他字段引用！'})
    #return HttpResponse(json_data)

    data.delete()
    json_data = json.dumps({'status':True,'info':''})

    return HttpResponse(json_data)

@login_required
@commons.permission_validate
def serverbk_list(request):
    sqldata = Serverbk.objects.all()

    idcroom = Idcroom.objects.all() # 获取机房列表

    idcroom_dict = {}
    for idc in idcroom:
        idcroom_dict[idc.id] = idc.name

    if request.method == 'POST':
        if request.FILES['file']:
            filepath = commons.handle_upload_file(request.FILES['file'])
        return HttpResponseRedirect('backup/serverbk/list')


    mydict = {'sqldata':sqldata,
              'mynotice':'',
              'idcroom_dict':idcroom_dict,
              'nav_backup_serverbk_list':"true"
             }
    mydict['mynotice'] = commons.mynotice(request)

    return render(request,'backup/serverbk_list.html',mydict)


#解析Excel文件,并批量添加到数据库,序列号已存在的不添加但更新，并生成提示
@login_required
@commons.permission_validate
def serverbk_addmore(request):
    if request.method == 'GET':
        filepath = request.GET.get('filepath', '')
        try:
            data = xlrd.open_workbook(filepath)
            table = data.sheets()[0]
            nrows = table.nrows #行数，从0开始
            ncols = table.ncols #列数，从0开始
            colnames =  table.row_values(0) #某一行数据

            # 遍历excel,添加和更新数据
            add = 0
            update = 0
            for rownum in range(1,nrows):
                row = table.row_values(rownum)
                if row:
                    # 读取每一行每列的值并赋值
                    sn = row[0]
                    brand = row[1]
                    model = row[2]
                    cpu = row[3]
                    memory = row[4]
                    disk = row[5]
                    idcroom_id = int(row[6])
                    guarantee = str(int(row[7]))

                    buydate = row[8]
                    # 判断如果读取的表格年月日是浮点型就做日期格式转换，否则保持不变
                    if isinstance(buydate, float):
                        buydate = xlrd.xldate_as_tuple(int(buydate),0) #格式化读取的excel中的日期（默认1900-based）
                        buydate = "%d-%d-%d"%(buydate[0],buydate[1],buydate[2]) #格式化为2016-06-14格式

                    comment = row[9]
                    user = request.user.username


                    # 排重，根据sn字段, 发现已存在，就更新信息
                    if Serverbk.objects.filter(sn = sn):
                        olddata = Serverbk.objects.filter(sn = sn)
                        id = olddata[0].id

                        if olddata[0].brand != brand or \
                            olddata[0].model != model or \
                            olddata[0].cpu != cpu or \
                            olddata[0].memory != memory or \
                            olddata[0].disk != disk or \
                            olddata[0].idcroom_id != idcroom_id or \
                            olddata[0].comment != comment or \
                            olddata[0].guarantee != guarantee or \
                            olddata[0].buydate != buydate:

                            serverbk = Serverbk.objects.get(id = id)
                            serverbk.sn = sn
                            serverbk.brand = brand
                            serverbk.model = model
                            serverbk.cpu = cpu
                            serverbk.memory = memory
                            serverbk.disk = disk
                            serverbk.idcroom_id = idcroom_id
                            serverbk.user = user
                            serverbk.comment = comment
                            serverbk.guarantee = guarantee
                            serverbk.buydate = buydate

                            serverbk.save()
                            update += 1

                    else:
                        # 写入数据库
                        serverbk = Serverbk(
                            sn = sn,
                            brand = brand,
                            model = model,
                            cpu = cpu,
                            memory = memory,
                            disk = disk,
                            idcroom_id = idcroom_id,
                            guarantee = guarantee,
                            buydate = buydate,
                            comment = comment,
                            user = request.user.username,
                        )
                        serverbk.save()
                        add += 1
            time.sleep(2)
            json_data = json.dumps({"error":0,"info":"成功导入%d台服务器备件，更新%d台服务器备件"%(add,update)})
            return HttpResponse(json_data)

        except Exception,e:
            time.sleep(2)
            json_data = json.dumps({"error":1,"info":"导入出错，请联系管理员或者检查Excel文件格式是否与系统提供的模板一致并重新操作，错误代码：%s"%(str(e))})
            return HttpResponse(json_data)

# 硬盘备件的增删改查，批量导入
@login_required
@commons.permission_validate
def diskbk_add(request):

    idcroom = Idcroom.objects.all() # 获取机房列表

    # 状态，OrderedDict保持字典原来顺序
    STATUS = OrderedDict([
        ('backup','备件'),
        ('fault','故障'),
        ('scrap','报废'),
    ])

    mydict = {"mynotice": "", # 状态提示条
              "idcroom":idcroom,
              "status":STATUS
             }

    if request.method == 'POST':
        sn = request.POST.get('sn', '')
        brand = request.POST.get('brand', '')
        type = request.POST.get('type', '')
        capacity = request.POST.get('capacity', '')
        status = request.POST.get('status', '')
        idcroom_id = request.POST.get('idcroom_id', '')
        user = request.user.username
        comment = request.POST.get('comment', '')
        guarantee = request.POST.get('guarantee', '')
        buydate = request.POST.get('buydate', '')


        if sn == '' or brand == '' or type == '' or capacity == '' or guarantee == '' or buydate == '':
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，带星号（*）表单不能为空！")
            return render(request,'backup/diskbk_add.html',mydict)


        if Diskbk.objects.filter(sn=sn):
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，此序列号已存在！")
            return render(request,'backup/diskbk_add.html',mydict)

        diskbk = Diskbk(
            sn = sn,
            brand = brand,
            type = type,
            capacity = capacity,
            status = status,
            idcroom_id = idcroom_id,
            user = user,
            comment = comment,
            guarantee = guarantee,
            buydate = buydate,
        )
        diskbk.save()
        commons.mynotice(request,"add","success")
        return HttpResponseRedirect("/backup/diskbk/list/")

    return render(request,'backup/diskbk_add.html',mydict)

@login_required
@commons.permission_validate
def diskbk_update(request,id):

    #id = request.REQUEST.get('id')
    sqldata = Diskbk.objects.get(id=id)
    idcroom = Idcroom.objects.all() # 获取机房列表

    # 状态，OrderedDict保持字典原来顺序
    STATUS = OrderedDict([
        ('backup','备件'),
        ('fault','故障'),
        ('scrap','报废'),
    ])

    mydict = {"sqldata":sqldata,
              "mynotice":"", # 状态提示条
              "idcroom":idcroom,
              "status":STATUS
             }

    if request.method == 'POST':
        sn = request.POST.get('sn', '')
        brand = request.POST.get('brand', '')
        type = request.POST.get('type', '')
        capacity = request.POST.get('capacity', '')
        status = request.POST.get('status', '')
        idcroom_id = request.POST.get('idcroom_id', '')
        user = request.user.username
        comment = request.POST.get('comment', '')
        guarantee = request.POST.get('guarantee', '')
        buydate = request.POST.get('buydate', '')


        if sn == '' or brand == '' or type == '' or capacity == '' or guarantee == '' or buydate == '':
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，带星号（*）表单不能为空！")
            return render(request,'backup/diskbk_update.html',mydict)


        if sqldata.sn != sn and len(Idcroom.objects.filter(sn=sn)) >= 1:
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，此序列号已存在！")
            return render(request,'backup/diskbk_update.html',mydict)


        diskbk = Diskbk.objects.get(id = id)
        diskbk.sn = sn
        diskbk.brand = brand
        diskbk.type = type
        diskbk.capacity = capacity
        diskbk.status = status
        diskbk.idcroom_id = idcroom_id
        diskbk.user = user
        diskbk.comment = comment
        diskbk.guarantee = guarantee
        diskbk.buydate = buydate

        diskbk.save()
        commons.mynotice(request,"update","success")
        return HttpResponseRedirect("/backup/diskbk/list/")

    return render(request,'backup/diskbk_update.html',mydict)

@login_required
@commons.permission_validate
def diskbk_del(request,id):
    id = int(id)
    data = Diskbk.objects.get(id=id)
    # 如果数据被其他字段引用，则不删除，弹出提示
    #json_data = json.dumps({'status':False,'info':'此数据有正在被其他字段引用！'})
    #return HttpResponse(json_data)

    data.delete()
    json_data = json.dumps({'status':True,'info':''})

    return HttpResponse(json_data)

@login_required
@commons.permission_validate
def diskbk_list(request):
    sqldata = Diskbk.objects.all()

    idcroom = Idcroom.objects.all() # 获取机房列表

    # 状态，OrderedDict保持字典原来顺序
    STATUS = OrderedDict([
        ('backup','备件'),
        ('fault','故障'),
        ('scrap','报废'),
    ])

    idcroom_dict = {}
    for idc in idcroom:
        idcroom_dict[idc.id] = idc.name


    mydict = {'sqldata':sqldata,
              'mynotice':'',
              'idcroom_dict':idcroom_dict,
              'status':STATUS,
              'nav_backup_diskbk_list':"true"
             }
    mydict['mynotice'] = commons.mynotice(request)

    return render(request,'backup/diskbk_list.html',mydict)


#解析Excel文件,并批量添加到数据库,序列号已存在的不添加但更新，并生成提示
@login_required
@commons.permission_validate
def diskbk_addmore(request):
    if request.method == 'GET':
        filepath = request.GET.get('filepath', '')
        try:
            data = xlrd.open_workbook(filepath)
            table = data.sheets()[0]
            nrows = table.nrows #行数，从0开始
            ncols = table.ncols #列数，从0开始
            colnames =  table.row_values(0) #某一行数据

            # 遍历excel,添加和更新数据
            add = 0
            update = 0
            for rownum in range(1,nrows):
                row = table.row_values(rownum)
                if row:
                    # 读取每一行每列的值并赋值
                    sn = row[0]
                    brand = row[1]
                    type = row[2]
                    capacity = row[3]
                    idcroom_id = int(row[4])
                    guarantee = str(int(row[5]))
                    buydate = row[6]

                    # 判断如果读取的表格年月日是浮点型就做日期格式转换，否则保持不变
                    if isinstance(buydate, float):
                        buydate = xlrd.xldate_as_tuple(int(buydate),0) #格式化读取的excel中的日期（默认1900-based）
                        buydate = "%d-%d-%d"%(buydate[0],buydate[1],buydate[2]) #格式化为2016-06-14格式

                    comment = row[7]
                    user = request.user.username
                    status = "backup" # 状态自动设置为备件


                    # 排重，根据sn字段, 发现已存在，就更新信息
                    if Diskbk.objects.filter(sn = sn):
                        olddata = Diskbk.objects.filter(sn = sn)
                        id = olddata[0].id

                        if olddata[0].brand != brand or \
                            olddata[0].type != type or \
                            olddata[0].capacity != capacity or \
                            olddata[0].idcroom_id != idcroom_id or \
                            olddata[0].status != status or \
                            olddata[0].comment != comment or \
                            olddata[0].guarantee != guarantee or \
                            olddata[0].buydate != buydate:

                            diskbk = Diskbk.objects.get(id = id)
                            diskbk.sn = sn
                            diskbk.brand = brand
                            diskbk.type = type
                            diskbk.capacity = capacity
                            diskbk.status = status
                            diskbk.idcroom_id = idcroom_id
                            diskbk.user = user
                            diskbk.comment = comment
                            diskbk.guarantee = guarantee
                            diskbk.buydate = buydate

                            diskbk.save()
                            update += 1

                    else:
                        # 写入数据库
                        diskbk = Diskbk(
                            sn = sn,
                            brand = brand,
                            type = type,
                            capacity = capacity,
                            status = status,
                            idcroom_id = idcroom_id,
                            guarantee = guarantee,
                            buydate = buydate,
                            comment = comment,
                            user = request.user.username,
                        )
                        diskbk.save()
                        add += 1
            time.sleep(2)
            json_data = json.dumps({"error":0,"info":"成功导入%d块硬盘备件，更新%d块硬盘备件"%(add,update)})
            return HttpResponse(json_data)
            #return HttpResponseRedirect('backup/diskbk/list')

        except Exception,e:
            #print str(e)
            time.sleep(2)
            json_data = json.dumps({"error":1,"info":"导入出错，请联系管理员或者检查Excel文件格式是否与系统提供的模板一致并重新操作，错误代码：%s"%(str(e))})
            return HttpResponse(json_data)


# 内存备件的增删改查，批量导入
@login_required
@commons.permission_validate
def memorybk_add(request):

    idcroom = Idcroom.objects.all() # 获取机房列表

    # 状态，OrderedDict保持字典原来顺序
    STATUS = OrderedDict([
        ('backup','备件'),
        ('fault','故障'),
        ('scrap','报废'),
    ])

    mydict = {"mynotice": "", # 状态提示条
              "idcroom":idcroom,
              "status":STATUS
             }

    if request.method == 'POST':
        sn = request.POST.get('sn', '')
        brand = request.POST.get('brand', '')
        type = request.POST.get('type', '')
        capacity = request.POST.get('capacity', '')
        status = request.POST.get('status', '')
        idcroom_id = request.POST.get('idcroom_id', '')
        user = request.user.username
        comment = request.POST.get('comment', '')
        guarantee = request.POST.get('guarantee', '')
        buydate = request.POST.get('buydate', '')


        if sn == '' or brand == '' or type == '' or capacity == '' or guarantee == '' or buydate == '':
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，带星号（*）表单不能为空！")
            return render(request,'backup/memorybk_add.html',mydict)


        if Memorybk.objects.filter(sn=sn):
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，此序列号已存在！")
            return render(request,'backup/memorybk_add.html',mydict)



        memorybk = Memorybk(
            sn = sn,
            brand = brand,
            type = type,
            capacity = capacity,
            status = status,
            idcroom_id = idcroom_id,
            user = user,
            comment = comment,
            guarantee = guarantee,
            buydate = buydate,
        )
        memorybk.save()
        commons.mynotice(request,"add","success")
        return HttpResponseRedirect("/backup/memorybk/list/")

    return render(request,'backup/memorybk_add.html',mydict)

@login_required
@commons.permission_validate
def memorybk_update(request,id):

    #id = request.REQUEST.get('id')
    sqldata = Memorybk.objects.get(id=id)
    idcroom = Idcroom.objects.all() # 获取机房列表

    # 状态，OrderedDict保持字典原来顺序
    STATUS = OrderedDict([
        ('backup','备件'),
        ('fault','故障'),
        ('scrap','报废'),
    ])

    mydict = {"sqldata":sqldata,
              "mynotice":"", # 状态提示条
              "idcroom":idcroom,
              "status":STATUS
             }

    if request.method == 'POST':
        sn = request.POST.get('sn', '')
        brand = request.POST.get('brand', '')
        type = request.POST.get('type', '')
        capacity = request.POST.get('capacity', '')
        status = request.POST.get('status', '')
        idcroom_id = request.POST.get('idcroom_id', '')
        user = request.user.username
        comment = request.POST.get('comment', '')
        guarantee = request.POST.get('guarantee', '')
        buydate = request.POST.get('buydate', '')


        if sn == '' or brand == '' or type == '' or capacity == '' or guarantee == '' or buydate == '':
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，带星号（*）表单不能为空！")
            return render(request,'backup/memorybk_update.html',mydict)


        memorybk = Memorybk.objects.get(id = id)
        memorybk.sn = sn
        memorybk.brand = brand
        memorybk.type = type
        memorybk.capacity = capacity
        memorybk.status = status
        memorybk.idcroom_id = idcroom_id
        memorybk.user = user
        memorybk.comment = comment
        memorybk.guarantee = guarantee
        memorybk.buydate = buydate

        memorybk.save()
        commons.mynotice(request,"update","success")
        return HttpResponseRedirect("/backup/memorybk/list/")

    return render(request,'backup/memorybk_update.html',mydict)

@login_required
@commons.permission_validate
def memorybk_del(request,id):
    id = int(id)
    data = Memorybk.objects.get(id=id)
    # 如果数据被其他字段引用，则不删除，弹出提示
    #json_data = json.dumps({'status':False,'info':'此数据有正在被其他字段引用！'})
    #return HttpResponse(json_data)

    data.delete()
    json_data = json.dumps({'status':True,'info':''})

    return HttpResponse(json_data)

@login_required
@commons.permission_validate
def memorybk_list(request):
    sqldata = Memorybk.objects.all()

    idcroom = Idcroom.objects.all() # 获取机房列表

    # 状态，OrderedDict保持字典原来顺序
    STATUS = OrderedDict([
        ('backup','备件'),
        ('fault','故障'),
        ('scrap','报废'),
    ])

    idcroom_dict = {}
    for idc in idcroom:
        idcroom_dict[idc.id] = idc.name

    mydict = {'sqldata':sqldata,
              'mynotice':'',
              'idcroom_dict':idcroom_dict,
              'status':STATUS,
              'nav_backup_memorybk_list':"true"
             }

    mydict['mynotice'] = commons.mynotice(request)

    return render(request,'backup/memorybk_list.html',mydict)


#解析Excel文件,并批量添加到数据库,序列号已存在的不添加但更新，并生成提示
@login_required
@commons.permission_validate
def memorybk_addmore(request):
    if request.method == 'GET':
        filepath = request.GET.get('filepath', '')
        try:
            data = xlrd.open_workbook(filepath)
            table = data.sheets()[0]
            nrows = table.nrows #行数，从0开始
            ncols = table.ncols #列数，从0开始
            colnames =  table.row_values(0) #某一行数据

            # 遍历excel,添加和更新数据
            add = 0
            for rownum in range(1,nrows):
                row = table.row_values(rownum)
                if row:
                    # 读取每一行每列的值并赋值
                    sn = row[0]
                    brand = row[1]
                    type = row[2]
                    capacity = row[3]
                    idcroom_id = int(row[4])
                    guarantee = str(int(row[5]))
                    buydate = row[6]

                    # 判断如果读取的表格年月日是浮点型就做日期格式转换，否则保持不变
                    if isinstance(buydate, float):
                        buydate = xlrd.xldate_as_tuple(int(buydate),0) #格式化读取的excel中的日期（默认1900-based）
                        buydate = "%d-%d-%d"%(buydate[0],buydate[1],buydate[2]) #格式化为2016-06-14格式

                    comment = row[7]
                    user = request.user.username
                    status = "backup" # 状态自动设置为备件


                    # 写入数据库
                    memorybk = Memorybk(
                        sn = sn,
                        brand = brand,
                        type = type,
                        capacity = capacity,
                        status = status,
                        idcroom_id = idcroom_id,
                        guarantee = guarantee,
                        buydate = buydate,
                        comment = comment,
                        user = user,
                    )
                    memorybk.save()
                    add += 1
            time.sleep(2)
            json_data = json.dumps({"error":0,"info":"成功导入%d条内存备件"%(add)})
            return HttpResponse(json_data)

        except Exception,e:
            time.sleep(2)
            json_data = json.dumps({"error":1,"info":"导入出错，请联系管理员或者检查Excel文件格式是否与系统提供的模板一致并重新操作，错误代码：%s"%(str(e))})
            return HttpResponse(json_data)
