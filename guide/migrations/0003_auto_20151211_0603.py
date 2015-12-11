# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0002_article_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='body_markup_type',
            field=models.CharField(default='markdown', choices=[('', '--'), ('markdown', 'markdown')], max_length=30),
        ),
    ]
