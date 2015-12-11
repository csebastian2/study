# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import markupfield.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('modification_date', models.DateTimeField(blank=True, null=True, verbose_name='Modification date')),
                ('body', markupfield.fields.MarkupField(rendered_field=True, verbose_name='Body')),
                ('body_markup_type', models.CharField(max_length=30, default=None, choices=[('', '--'), ('markdown', 'markdown')])),
                ('_body_rendered', models.TextField(editable=False)),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='guide_article', null=True, verbose_name='Author', to=settings.AUTH_USER_MODEL, related_name='guide_articles')),
            ],
            options={
                'verbose_name_plural': 'Articles',
                'verbose_name': 'Article',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(verbose_name='Slug')),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('color', models.CharField(max_length=32, default='default', choices=[('default', 'Default'), ('red', 'Red'), ('green', 'Green'), ('yellow', 'Yellow'), ('blue', 'Blue')], verbose_name='Color')),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'verbose_name': 'Tag',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='guide.Tag', related_name='articles', related_query_name='article', verbose_name='Tags'),
        ),
    ]
