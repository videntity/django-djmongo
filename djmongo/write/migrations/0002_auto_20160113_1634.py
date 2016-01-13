# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('write', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='writeapihttpauth',
            options={'ordering': ('-creation_date',), 'get_latest_by': 'creation_date', 'verbose_name': 'Write API with HTTPAuth', 'verbose_name_plural': 'Write APIs with HTTPAuth'},
        ),
        migrations.AlterModelOptions(
            name='writeapiip',
            options={'ordering': ('-creation_date',), 'get_latest_by': 'creation_date', 'verbose_name': 'Write API with IP Address Auth', 'verbose_name_plural': 'Write APIs with IP Address Auth'},
        ),
        migrations.AddField(
            model_name='writeapihttpauth',
            name='group',
            field=models.ForeignKey(blank=True, to='auth.Group', null=True),
        ),
        migrations.AddField(
            model_name='writeapihttpauth',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='writeapiip',
            name='group',
            field=models.ForeignKey(blank=True, to='auth.Group', null=True),
        ),
        migrations.AddField(
            model_name='writeapiip',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='writeapioauth2',
            name='group',
            field=models.ForeignKey(blank=True, to='auth.Group', null=True),
        ),
        migrations.AddField(
            model_name='writeapioauth2',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
