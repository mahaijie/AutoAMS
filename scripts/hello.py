# 执行方法：python manage.py runscript hello
# 需要安装django-extension，pip install django-extension

from idcroom.models import Idcroom
def run():
    sqldata = Idcroom.objects.all()
    for data in sqldata:
        print data.name
    print 'Hello MHJ'
