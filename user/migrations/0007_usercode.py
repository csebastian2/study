# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20151201_0054'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('code', models.CharField(verbose_name='Code', max_length=64)),
                ('type', models.CharField(choices=[('account_activation', 'Account activation'), ('password_reset', 'Password reset')], verbose_name='Type', max_length=32)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('expiration_date', models.DateTimeField(verbose_name='Expiration date', blank=True, null=True)),
                ('is_used', models.BooleanField(default=False, verbose_name='Is used?')),
                ('user', models.ForeignKey(related_name='codes', related_query_name='code', verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User codes',
                'verbose_name': 'User code',
            },
        ),
    ]
