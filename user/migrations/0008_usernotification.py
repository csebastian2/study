# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_usercode'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('message', models.CharField(verbose_name='Message', max_length=255)),
                ('url', models.URLField(blank=True, verbose_name='URL', null=True)),
                ('read', models.BooleanField(verbose_name='Read', default=False)),
                ('creation_date', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='notifications', verbose_name='User', related_query_name='notification')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
    ]
