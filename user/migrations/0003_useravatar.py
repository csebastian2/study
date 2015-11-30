# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20151127_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAvatar',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('picture', models.ImageField(upload_to='user/avatars/', verbose_name='Picture', blank=True, default=None, null=True)),
                ('last_update', models.DateTimeField(verbose_name='Last update', blank=True, default=None, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='User', related_query_name='avatar', related_name='avatar')),
            ],
            options={
                'verbose_name': 'Avatar',
                'verbose_name_plural': 'Avatars',
            },
        ),
    ]
