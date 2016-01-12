# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WriteAPIHTTPAuth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('database_name', models.CharField(max_length=100)),
                ('collection_name', models.CharField(max_length=100)),
                ('json_schema', models.TextField(default=b'{}', help_text=b'Default "{}", means no JSONschema.', max_length=2048, verbose_name=b'JSON Schema')),
                ('creation_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-creation_date',),
                'get_latest_by': 'creation_date',
                'verbose_name': 'Write API with HTTPAuth Auth',
                'verbose_name_plural': 'Write APIs with HTTPAuth Auth',
            },
        ),
        migrations.CreateModel(
            name='WriteAPIIP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('database_name', models.CharField(max_length=100)),
                ('collection_name', models.CharField(max_length=100)),
                ('json_schema', models.TextField(default=b'{}', help_text=b'Default "{}", means no JSONschema.', max_length=2048, verbose_name=b'JSON Schema')),
                ('from_ip', models.TextField(default=b'127.0.0.1', help_text=b'Only accept requests from a IP in this list (separated by whitespace). 0.0.0.0 means all.', max_length=2048, verbose_name=b'From IPs')),
                ('creation_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-creation_date',),
                'get_latest_by': 'creation_date',
                'verbose_name': 'Write API with IP address Auth',
                'verbose_name_plural': 'Write APIs with IP address Auth',
            },
        ),
        migrations.CreateModel(
            name='WriteAPIoAuth2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('database_name', models.CharField(max_length=100)),
                ('collection_name', models.CharField(max_length=100)),
                ('json_schema', models.TextField(default=b'{}', help_text=b'Default "{}", means no JSONschema.', max_length=2048, verbose_name=b'JSON Schema')),
                ('creation_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-creation_date',),
                'get_latest_by': 'creation_date',
                'verbose_name': 'Write API with oAuth2 Auth',
                'verbose_name_plural': 'Write APIs with oAuth2 Auth',
            },
        ),
    ]
