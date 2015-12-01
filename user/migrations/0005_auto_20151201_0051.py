# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import user.storage
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20151130_0417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useravatar',
            name='picture',
            field=models.ImageField(upload_to=user.models.avatar_path, verbose_name='Picture', storage=user.storage.OverwriteStorage, null=True, default=None, blank=True),
        ),
    ]
