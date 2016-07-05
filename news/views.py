# -*- coding: utf-8 -*-
# Author:马海杰
# Email:mahaijie123@163.com

from AutoAMS import commons
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Column, Article
from django import forms
from DjangoUeditor.forms import UEditorField
from django.contrib.auth.decorators import login_required
import json

@login_required
@commons.permission_validate
def column_add(request):
    class TestUEditorForm(forms.Form):
        intro=UEditorField("",initial="",width=782,height=400,imagePath="uploads/images/",toolbars='full', filePath='uploads/files/')
    form = TestUEditorForm()

    mynotice = "" # 状态提示条
    mydict = {"form": form,
              "mynotice": mynotice,
             }

    if request.method == 'POST':
        name = request.POST.get('name', '')
        slug = request.POST.get('slug', '')
        intro = request.POST.get('intro', '')
        nav_display = request.POST.get('nav_display', '')
        home_display = request.POST.get('home_display', '')

        if name == '' or slug == '' or intro == '':
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，带星号（*）表单不能为空！")
            return render(request,'news/column_add.html',mydict)

        if Column.objects.filter(name=name):
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，此分类已存在！")
            return render(request,'news/column_add.html',mydict)

        if Column.objects.filter(slug=slug):
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，此网址已存在！")
            return render(request,'news/column_add.html',mydict)

        column = Column(
            name = name,
            slug = slug,
            intro = intro,
            nav_display = nav_display,
            home_display = home_display,
        )
        column.save()
        commons.mynotice(request,"add","success")
        return HttpResponseRedirect("/news/column/list/")

    return render(request,'news/column_add.html',mydict)

@login_required
@commons.permission_validate
def column_update(request,id):

    #id = request.REQUEST.get('id')
    sqldata = Column.objects.get(id=id)

    class TestUEditorForm(forms.Form):
        intro=UEditorField("",initial=sqldata.intro,width=782,height=400,imagePath="uploads/images/",toolbars='full', filePath='uploads/files/')
    form = TestUEditorForm()

    mynotice = "" # 状态提示条
    mydict = {"form": form,
              "sqldata":sqldata,
              "mynotice":mynotice,
             }

    if request.method == 'POST':
        name = request.POST.get('name', '')
        slug = request.POST.get('slug', '')
        intro = request.POST.get('intro', '')
        nav_display = request.POST.get('nav_display', '')
        home_display = request.POST.get('home_display', '')

        if name == ''or slug == '' or intro == '':
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，带星号（*）表单不能为空！")
            return render(request,'news/column_update.html',mydict)

        if sqldata.name != name and len(Column.objects.filter(name=name)) >= 1:
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，此分类已存在！")
            return render(request,'news/column_update.html',mydict)

        if sqldata.slug != slug and len(Column.objects.filter(slug=slug)) > 1:
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，此网址已存在！")
            return render(request,'news/column_update.html',mydict)

        column = Column.objects.get(id = id)
        column.name = name
        column.slug = slug
        column.intro = intro
        column.nav_display = nav_display
        column.home_display = home_display

        column.save()
        commons.mynotice(request,"update","success")
        return HttpResponseRedirect("/news/column/list/")

    return render(request,'news/column_update.html',mydict)

@login_required
@commons.permission_validate
def column_del(request,id):
    id = int(id)
    data = Column.objects.get(id=id)
    # 如果数据被其他字段引用，则不删除，弹出提示
    #json_data = json.dumps({'status':False,'info':'此数据有正在被其他字段引用！'})
    #return HttpResponse(json_data)

    data.delete()
    json_data = json.dumps({'status':True,'info':''})

    return HttpResponse(json_data)

@login_required
@commons.permission_validate
def column_list(request):
    sqldata = Column.objects.all()

    mynotice = ""
    if request.method == 'GET':
        action = request.GET.get('action')
        if action == "add":
            mynotice = commons.mynotice("success","恭喜您，添加成功！")
        elif action == "update":
            mynotice = commons.mynotice("success","恭喜您，更新成功！")
        elif action == "del":
            mynotice = commons.mynotice("success","恭喜您，删除成功！")

    return render(request,'news/column_list.html',{'sqldata':sqldata,'mynotice':mynotice,'nav_news_column_list':"true"})


@login_required
@commons.permission_validate
def article_add(request):
    class TestUEditorForm(forms.Form):
        content=UEditorField("",initial="",width=782,height=400,imagePath="uploads/images/",toolbars='full', filePath='uploads/files/')
    form = TestUEditorForm()

    mynotice = "" # 状态提示条
    columns = Column.objects.all() # 获取分类列表
    mydict = {"form": form,
              "mynotice": mynotice,
              "columns": columns,
             }

    if request.method == 'POST':
        title = request.POST.get('title', '')
        column_id = request.POST.get('column_id', '')
        author = request.user.username # 添加文章时，作者字段获取系统登录用户
        content = request.POST.get('content', '')
        published = request.POST.get('published', '')

        if title == '' or content == ''or column_id == '':
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，带星号（*）表单不能为空！")
            return render(request,'news/article_add.html',mydict)

        if Article.objects.filter(title=title):
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，此文章已存在！")
            return render(request,'news/article_add.html',mydict)


        article = Article(
            title = title,
            column_id = int(column_id),
            author = author,
            content = content,
            published = published,
        )
        article.save()
        commons.mynotice(request,"add","success")
        return HttpResponseRedirect("/news/article/list/")

    return render(request,'news/article_add.html',mydict)

@login_required
@commons.permission_validate
def article_update(request,id):

    #id = request.REQUEST.get('id')
    sqldata = Article.objects.get(id=id)

    class TestUEditorForm(forms.Form):
        # initial 指定Ueditor内容
        content=UEditorField("",initial=sqldata.content,width=782,height=400,imagePath="uploads/images/",toolbars='full', filePath='uploads/files/')
    form = TestUEditorForm()

    mynotice = "" # 状态提示条
    columns = Column.objects.all() # 获取分类列表

    mydict = {"form": form,
              "sqldata":sqldata,
              "mynotice":mynotice,
              "columns":columns,
             }

    if request.method == 'POST':
        title = request.POST.get('title', '')
        column_id = request.POST.get('column_id', '')
        content = request.POST.get('content', '')
        published = request.POST.get('published', '')

        if title == '' or content == '':
            mydict['mynotice'] = commons.mynotice(request,"update","error","更新失败，带星号（*）表单不能为空！")
            return render(request,'news/article_update.html',mydict)

        if sqldata.title != title and len(Article.objects.filter(title=title)) >= 1:
            mydict['mynotice'] = commons.mynotice(request,"add","error","添加失败，此文章已存在！")
            return render(request,'news/article_update.html',mydict)


        article = Article.objects.get(id = id)
        article.title = title
        article.column_id = column_id
        article.content = content
        article.published = published

        article.save()
        commons.mynotice(request,"update","success")
        return HttpResponseRedirect("/news/article/list/")

    return render(request,'news/article_update.html',mydict)

@login_required
@commons.permission_validate
def article_del(request,id):
    id = int(id)
    data = Article.objects.get(id=id)
    # 如果数据被其他字段引用，则不删除，弹出提示
    #json_data = json.dumps({'status':False,'info':'此数据有正在被其他字段引用！'})
    #return HttpResponse(json_data)

    data.delete()
    json_data = json.dumps({'status':True,'info':''})

    return HttpResponse(json_data)

@login_required
@commons.permission_validate
def article_list(request):
    sqldata = Article.objects.all()
    columns = Column.objects.all() # 获取分类列表

    columns_dict = {}
    for column in columns:
        columns_dict[column.id] = column.name

    mydict = {'sqldata':sqldata,
              'mynotice':'',
              'columns_dict':columns_dict,
              'nav_news_article_list':"true",
              }
    mydict['mynotice'] = commons.mynotice(request)

    return render(request,'news/article_list.html',mydict)

@login_required
@commons.permission_validate
def article_view(request,id):
    sqldata = Article.objects.get(id=id)
    columns = Column.objects.all() # 获取分类列表

    # 更新阅读次数
    new_count = sqldata.count + 1
    Article.objects.filter(id=id).update(count=new_count)

    columns_dict = {}
    for column in columns:
        columns_dict[column.id] = column.name

    mydict = {'sqldata':sqldata,
              'columns_dict':columns_dict,
              'nav_news_article_list':"true",
              }

    return render(request,'news/article_view.html',mydict)
