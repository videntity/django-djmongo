# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('write', '0003_auto_20160113_1638'),
    ]

    operations = [
        migrations.RenameField(
            model_name='writeapihttpauth',
            old_name='user',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='writeapiip',
            old_name='user',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='writeapioauth2',
            old_name='user',
            new_name='created_by',
        ),
        migrations.AlterField(
            model_name='writeapihttpauth',
            name='json_schema',
            field=models.TextField(default=b'{}', help_text=b'Default "{}", means no JSON Schema.', max_length=2048, verbose_name=b'JSON Schema'),
        ),
        migrations.AlterField(
            model_name='writeapiip',
            name='json_schema',
            field=models.TextField(default=b'{}', help_text=b'Default "{}", means no JSON Schema.', max_length=2048, verbose_name=b'JSON Schema'),
        ),
        migrations.AlterField(
            model_name='writeapioauth2',
            name='json_schema',
            field=models.TextField(default=b'{}', help_text=b'Default "{}", means no JSON Schema.', max_length=2048, verbose_name=b'JSON Schema'),
        ),
    ]
