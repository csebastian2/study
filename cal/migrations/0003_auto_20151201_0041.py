# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0002_task_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'verbose_name_plural': 'Tasks', 'verbose_name': 'Task'},
        ),
    ]
