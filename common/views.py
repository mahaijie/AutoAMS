# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json,datetime,os,time,random
from AutoAMS import settings

# Create your views here.

@login_required
def index(request):
    return render(request,'common/index.html',locals())

@login_required
def noaccess(request):
    return render(request,'common/NoAccess.html',locals())


#上传文件
@csrf_exempt
def my_upload_file(request):
    ext_allowed = {}
    ext_allowed["image"] = ['gif', 'jpg', 'jpeg', 'png']
    ext_allowed["flash"] = ["swf", "flv"]
    ext_allowed["media"] = ["swf", "flv", "mp3", "wav", "wma", "wmv", "mid", "avi", "mpg", "asf", "rm", "rmvb"]
    ext_allowed["file"] = ["doc", "docx", "xls", "xlsx", "ppt", "htm", "html", "txt", "zip", "rar", "gz" , "bz2"]
    ext_allowed["excel"] = ["xls", "xlsx", "csv"]

    max_size = 1000000  # 限制大小10MB
    dir_name = request.GET["type"]
    save_dir = 'uploads/' + dir_name + time.strftime('/%Y%m%d/')
    save_path = settings.MEDIA_ROOT + '/' + save_dir
    save_url = settings.MEDIA_URL  + save_dir

    if request.method == 'POST':
        file_content = request.FILES['file']

        if not file_content.name:
            return HttpResponse(json.dumps(
                { 'error': 1, 'message': u'请选择要上传的文件' }
            ))

        ext = file_content.name.split('.').pop()

        if ext not in ext_allowed[dir_name]:
            return HttpResponse(json.dumps(
                { 'error': 1, 'message': u'请上传后缀为%s的文件' %  ext_allowed[dir_name]}
            ))

        if file_content.size > max_size:
            return HttpResponse(json.dumps(
                { 'error': 1, 'message': u'上传的文件大小不能超过10MB'}
            ))

        if not os.path.isdir(save_path):
            os.makedirs(save_path)

        new_file = time.strftime('%Y%m%d%H%M%S_') + str(random.randint(0,99999)) + "_" + file_content.name

        destination = open(save_path+new_file, 'wb+')
        for chunk in file_content.chunks():
            destination.write(chunk)
        destination.close()

        return HttpResponse(json.dumps(
                { 'error': 0, 'url': save_path + new_file}
        ))

