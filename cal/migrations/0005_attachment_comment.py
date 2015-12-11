# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cal', '0004_auto_20151201_0324'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(verbose_name='Creation date')),
                ('comment', models.CharField(null=True, verbose_name='Comment', blank=True, max_length=128)),
                ('file', models.FileField(verbose_name='File', upload_to='private/tasks/attachments')),
                ('author', models.ForeignKey(related_name='task_attachments', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Author', blank=True, related_query_name='task_attachment')),
                ('task', models.ForeignKey(related_name='attachments', to='cal.Task', verbose_name='Task', related_query_name='attachment')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('date_modified', models.DateTimeField(null=True, verbose_name='Modification date', blank=True)),
                ('text', models.TextField(verbose_name='Comment text', max_length=1000)),
                ('author', models.ForeignKey(related_name='task_comments', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Author', blank=True, related_query_name='task_comment')),
                ('task', models.ForeignKey(related_name='tasks', to='cal.Task', verbose_name='Task', related_query_name='task')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
    ]
