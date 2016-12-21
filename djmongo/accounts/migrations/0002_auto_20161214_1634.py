# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-14 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djmongo_accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='permission_name',
            field=models.CharField(choices=[('db-all', 'All MongoDB'), ('db-write', 'Write MongoDB'), ('db-read', 'Read MongoDB'), ('create-other-users', 'create-other-users'), ('create-any-socialgraph', 'create-any-socialgraph'), ('delete-any-socialgraph', 'delete-any-socialgraph')], max_length=256),
        ),
    ]
