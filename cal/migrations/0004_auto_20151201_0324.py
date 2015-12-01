# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0003_auto_20151201_0041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='calendar',
            field=models.ForeignKey(related_query_name='task', to='cal.Calendar', related_name='tasks', verbose_name='Calendar'),
        ),
    ]
