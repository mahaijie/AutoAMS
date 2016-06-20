# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idcroom', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='idcroom',
            old_name='content',
            new_name='comment',
        ),
    ]
