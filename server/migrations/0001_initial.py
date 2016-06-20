# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(max_length=256, verbose_name='\u5e8f\u5217\u53f7')),
                ('brand', models.CharField(max_length=256, verbose_name='\u54c1\u724c')),
                ('model', models.CharField(max_length=256, verbose_name='\u578b\u53f7')),
                ('cpu', models.TextField(default='', verbose_name='CPU')),
                ('memory', models.TextField(default='', verbose_name='\u5185\u5b58')),
                ('disk', models.TextField(default='', verbose_name='\u786c\u76d8')),
                ('network', models.TextField(default='', verbose_name='\u7f51\u5361')),
                ('ip', models.CharField(max_length=256, verbose_name='ip')),
                ('other_ip', models.CharField(max_length=256, verbose_name='\u5176\u4ed6ip')),
                ('system', models.CharField(max_length=256, verbose_name='\u7cfb\u7edf')),
                ('position', models.CharField(max_length=256, verbose_name='\u4f4d\u7f6e')),
                ('user', models.CharField(max_length=256, verbose_name='\u64cd\u4f5c\u5458')),
                ('company', models.CharField(max_length=256, verbose_name='\u516c\u53f8')),
                ('department', models.CharField(max_length=256, verbose_name='\u90e8\u95e8')),
                ('principal', models.CharField(max_length=256, verbose_name='\u8d1f\u8d23\u4eba')),
                ('servicetype', models.CharField(max_length=256, verbose_name='\u670d\u52a1\u7c7b\u578b')),
                ('comment', models.TextField(default='', verbose_name='\u5907\u6ce8')),
                ('guarantee', models.CharField(max_length=256, verbose_name='\u4fdd\u4fee\u5e74\u9650')),
                ('buydate', models.CharField(max_length=256, verbose_name='\u8d2d\u4e70\u65e5\u671f')),
                ('uptime', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4', null=True)),
            ],
        ),
    ]
