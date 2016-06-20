# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='status',
            field=models.CharField(default=datetime.datetime(2016, 6, 6, 9, 22, 23, 669000, tzinfo=utc), max_length=256, verbose_name='\u64cd\u4f5c\u5458'),
            preserve_default=False,
        ),
    ]
