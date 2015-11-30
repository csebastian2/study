# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='Name')),
                ('date_created', models.DateTimeField(verbose_name='Created', auto_now_add=True)),
                ('author', models.ForeignKey(verbose_name='Author', related_query_name='author', to=settings.AUTH_USER_MODEL, related_name='authors')),
                ('members', models.ManyToManyField(verbose_name='Members', related_query_name='members', related_name='members', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Calendars',
                'verbose_name': 'Calendar',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('date_created', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('date_modified', models.DateTimeField(blank=True, verbose_name='Modify date', null=True)),
                ('date_start', models.DateTimeField(verbose_name='Start date')),
                ('date_end', models.DateTimeField(verbose_name='End date')),
                ('author', models.ForeignKey(verbose_name='Author', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('calendar', models.ForeignKey(to='cal.Calendar', verbose_name='Calendar')),
            ],
            options={
                'verbose_name': 'Entry',
                'verbose_name_plural': 'Entries',
            },
        ),
        migrations.AlterUniqueTogether(
            name='calendar',
            unique_together=set([('author', 'name')]),
        ),
    ]
