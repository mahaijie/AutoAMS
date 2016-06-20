# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idcroom', '0002_auto_20160606_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diskbk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(max_length=256, verbose_name='\u5e8f\u5217\u53f7')),
                ('brand', models.CharField(max_length=256, verbose_name='\u54c1\u724c')),
                ('type', models.CharField(max_length=256, verbose_name='\u7c7b\u578b')),
                ('capacity', models.CharField(max_length=256, verbose_name='\u5bb9\u91cf')),
                ('status', models.CharField(default='backup', max_length=10, verbose_name='\u72b6\u6001')),
                ('user', models.CharField(max_length=256, verbose_name='\u64cd\u4f5c\u5458')),
                ('comment', models.TextField(default='', verbose_name='\u5907\u6ce8')),
                ('guarantee', models.CharField(max_length=256, verbose_name='\u4fdd\u4fee\u5e74\u9650')),
                ('buydate', models.CharField(max_length=256, verbose_name='\u8d2d\u4e70\u65e5\u671f')),
                ('uptime', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4', null=True)),
                ('idcroom', models.ForeignKey(verbose_name='\u6240\u5728\u673a\u623f', to='idcroom.Idcroom')),
            ],
        ),
        migrations.CreateModel(
            name='Memorybk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(max_length=256, verbose_name='\u5e8f\u5217\u53f7')),
                ('brand', models.CharField(max_length=256, verbose_name='\u54c1\u724c')),
                ('type', models.CharField(max_length=256, verbose_name='\u7c7b\u578b')),
                ('capacity', models.CharField(max_length=256, verbose_name='\u5bb9\u91cf')),
                ('status', models.CharField(default='backup', max_length=10, verbose_name='\u72b6\u6001')),
                ('user', models.CharField(max_length=256, verbose_name='\u64cd\u4f5c\u5458')),
                ('comment', models.TextField(default='', verbose_name='\u5907\u6ce8')),
                ('guarantee', models.CharField(max_length=256, verbose_name='\u4fdd\u4fee\u5e74\u9650')),
                ('buydate', models.CharField(max_length=256, verbose_name='\u8d2d\u4e70\u65e5\u671f')),
                ('uptime', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4', null=True)),
                ('idcroom', models.ForeignKey(verbose_name='\u6240\u5728\u673a\u623f', to='idcroom.Idcroom')),
            ],
        ),
        migrations.CreateModel(
            name='Serverbk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sn', models.CharField(max_length=256, verbose_name='\u5e8f\u5217\u53f7')),
                ('brand', models.CharField(max_length=256, verbose_name='\u54c1\u724c')),
                ('model', models.CharField(max_length=256, verbose_name='\u578b\u53f7')),
                ('cpu', models.TextField(default='', verbose_name='CPU')),
                ('memory', models.TextField(default='', verbose_name='\u5185\u5b58')),
                ('disk', models.TextField(default='', verbose_name='\u786c\u76d8')),
                ('user', models.CharField(max_length=256, verbose_name='\u64cd\u4f5c\u5458')),
                ('comment', models.TextField(default='', verbose_name='\u5907\u6ce8')),
                ('guarantee', models.CharField(max_length=256, verbose_name='\u4fdd\u4fee\u5e74\u9650')),
                ('buydate', models.CharField(max_length=256, verbose_name='\u8d2d\u4e70\u65e5\u671f')),
                ('uptime', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4', null=True)),
                ('idcroom', models.ForeignKey(verbose_name='\u6240\u5728\u673a\u623f', to='idcroom.Idcroom')),
            ],
        ),
    ]
