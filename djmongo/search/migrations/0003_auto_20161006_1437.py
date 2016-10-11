# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-06 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
        ('search', '0002_auto_20160928_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='HTTPAuthReadAPI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('database_name', models.CharField(max_length=256)),
                ('collection_name', models.CharField(max_length=256)),
                ('slug', models.SlugField(blank=True, help_text=b'Give your API a unique name', max_length=100)),
                ('search_keys', models.TextField(blank=True, default=b'', help_text=b'The default, blank, returns\n                                                all keys. Providing a list of\n                                                keys, separated by whitespace,\n                                                limits the API search to only\n                                                these keys.', max_length=4096)),
                ('groups', models.ManyToManyField(blank=True, related_name='djmongo_http_auth_read_api', to='auth.Group')),
            ],
            options={
                'verbose_name': 'Search API using HTTPAuth',
                'verbose_name_plural': 'Search APIs using HTTPAuth',
            },
        ),
        migrations.AlterUniqueTogether(
            name='databaseaccesscontrol',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='databaseaccesscontrol',
            name='groups',
        ),
        migrations.AddField(
            model_name='publicreadapi',
            name='slug',
            field=models.SlugField(blank=True, help_text=b'Give your API a unique name', max_length=100),
        ),
        migrations.DeleteModel(
            name='DatabaseAccessControl',
        ),
        migrations.AlterUniqueTogether(
            name='httpauthreadapi',
            unique_together=set([('database_name', 'collection_name')]),
        ),
    ]
