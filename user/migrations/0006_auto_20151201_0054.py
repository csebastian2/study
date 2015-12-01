# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import user.storage
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20151201_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useravatar',
            name='picture',
            field=models.ImageField(null=True, default=None, blank=True, verbose_name='Picture', upload_to=user.models.avatar_path, storage=user.storage.OverwriteStorage()),
        ),
    ]
