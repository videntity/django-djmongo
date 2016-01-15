# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aggregation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('pipeline', models.TextField(default=b'[]', max_length=20480, verbose_name=b'Pipeline')),
                ('database_name', models.CharField(max_length=256)),
                ('collection_name', models.CharField(max_length=256)),
                ('output_collection_name', models.CharField(help_text=b'The resulting collection. Do not include $out in your pipeline.', max_length=256)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('execute_now', models.BooleanField(default=False)),
                ('scheduled_job_in_process', models.BooleanField(default=False)),
                ('scheduled_job_completed_for_today', models.BooleanField(default=False)),
                ('scheduled_job_not_ran', models.BooleanField(default=True)),
                ('execute_everyday', models.BooleanField(default=False)),
                ('execute_sunday', models.BooleanField(default=False)),
                ('execute_monday', models.BooleanField(default=False)),
                ('execute_tuesday', models.BooleanField(default=False)),
                ('execute_wednesday', models.BooleanField(default=False)),
                ('execute_thursday', models.BooleanField(default=False)),
                ('execute_friday', models.BooleanField(default=False)),
                ('execute_saturday', models.BooleanField(default=False)),
                ('execute_time_1', models.TimeField(help_text=b'Use 24 hour time. (e.g. 20:30:00 for 8:30 pm)', verbose_name=b'Execute Time')),
                ('description', models.TextField(default=b'', max_length=1024, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-creation_date',),
                'get_latest_by': 'creation_date',
                'verbose_name_plural': 'Saved Aggregations',
            },
        ),
    ]
