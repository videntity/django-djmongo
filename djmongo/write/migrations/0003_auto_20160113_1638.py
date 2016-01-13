# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('write', '0002_auto_20160113_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='writeapihttpauth',
            name='group',
        ),
        migrations.RemoveField(
            model_name='writeapiip',
            name='group',
        ),
        migrations.RemoveField(
            model_name='writeapioauth2',
            name='group',
        ),
        migrations.AddField(
            model_name='writeapihttpauth',
            name='groups',
            field=models.ManyToManyField(related_name='djmongo_write_httpauth_groups', to='auth.Group', blank=True),
        ),
        migrations.AddField(
            model_name='writeapiip',
            name='groups',
            field=models.ManyToManyField(related_name='djmongo_write_ip_groups', to='auth.Group', blank=True),
        ),
        migrations.AddField(
            model_name='writeapioauth2',
            name='groups',
            field=models.ManyToManyField(related_name='djmongo_write_oauth_groups', to='auth.Group', blank=True),
        ),
    ]
