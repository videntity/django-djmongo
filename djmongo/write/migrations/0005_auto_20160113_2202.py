# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('write', '0004_auto_20160113_1640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='writeapiip',
            name='groups',
        ),
        migrations.AlterField(
            model_name='writeapihttpauth',
            name='groups',
            field=models.ManyToManyField(help_text='Use ctrl to select multiple groups. If no groups are selected blank, any user may access the API.', related_name='djmongo_write_httpauth_groups', to='auth.Group', blank=True),
        ),
        migrations.AlterField(
            model_name='writeapihttpauth',
            name='slug',
            field=models.SlugField(help_text='The slug is the unique part of the URL for your API.', unique=True, max_length=100),
        ),
    ]
