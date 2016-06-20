# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Idcroom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='\u673a\u623f\u540d\u79f0')),
                ('user', models.CharField(max_length=256, verbose_name='\u64cd\u4f5c\u5458')),
                ('content', models.TextField(default='', verbose_name='\u5907\u6ce8')),
            ],
        ),
    ]
