# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='registration_ip',
            field=models.GenericIPAddressField(null=True, verbose_name='IP Address', blank=True),
        ),
    ]
