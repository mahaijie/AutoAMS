# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com
# 执行方法：python manage.py runscript hello
# 需要安装django-extensions，pip install django-extensions

from idcroom.models import Idcroom

def run():
    sqldata = Idcroom.objects.all()
    for data in sqldata:
        print data.name
    print 'Hello MHJ'
