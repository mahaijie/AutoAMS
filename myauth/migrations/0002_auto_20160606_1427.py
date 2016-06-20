# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='intro',
        ),
        migrations.AddField(
            model_name='group',
            name='comment',
            field=models.TextField(default=b'', verbose_name=b'\xe5\x88\x86\xe7\xbb\x84\xe5\xa4\x87\xe6\xb3\xa8'),
        ),
        migrations.AlterField(
            model_name='user',
            name='group',
            field=models.ForeignKey(verbose_name=b'\xe6\x9d\x83\xe9\x99\x90\xe5\x88\x86\xe7\xbb\x84', to='myauth.Group'),
        ),
    ]
