# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0005_attachment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='_body_rendered',
            field=models.TextField(default='', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='body',
            field=markupfield.fields.MarkupField(verbose_name='Body', default='', rendered_field=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='body_markup_type',
            field=models.CharField(default='markdown', choices=[('', '--'), ('markdown', 'markdown')], max_length=30),
        ),
    ]
