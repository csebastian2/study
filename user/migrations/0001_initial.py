# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('email', models.EmailField(verbose_name='Email', unique=True, max_length=254)),
                ('username', models.CharField(validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9.@-_ ]+$', 'Valid name may contain letters and digits.')], verbose_name='Name', help_text='Required. 64 characters or fewer. May contain letters and digits.', max_length=64)),
                ('registration_date', models.DateTimeField(auto_now_add=True, verbose_name='Registration date')),
                ('registration_ip', models.GenericIPAddressField(verbose_name='IP Address')),
                ('is_active', models.BooleanField(verbose_name='Active', default=False)),
                ('is_staff', models.BooleanField(verbose_name='Staff', default=False)),
                ('groups', models.ManyToManyField(related_name='user_set', blank=True, related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(related_name='user_set', blank=True, related_query_name='user', help_text='Specific permissions for this user.', verbose_name='user permissions', to='auth.Permission')),
            ],
            options={
                'verbose_name': 'User profile',
                'verbose_name_plural': 'User profiles',
            },
        ),
        migrations.CreateModel(
            name='UserLogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date added')),
                ('type', models.CharField(verbose_name='Type', default='general', choices=[('general', 'General'), ('user', 'User'), ('error', 'Error')], max_length=16)),
                ('message', models.CharField(verbose_name='Message', max_length=255)),
                ('user', models.ForeignKey(related_name='log_entries', related_query_name='log_entry', verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User log entry',
                'verbose_name_plural': 'User log entries',
            },
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('session_key', models.CharField(verbose_name='Session key', max_length=40)),
                ('user', models.ForeignKey(related_name='session_references', related_query_name='session_reference', verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User session reference',
                'verbose_name_plural': 'User session references',
            },
        ),
    ]
