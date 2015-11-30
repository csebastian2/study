# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_useravatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useravatar',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='avatar', verbose_name='User', related_query_name='avatar'),
        ),
    ]
