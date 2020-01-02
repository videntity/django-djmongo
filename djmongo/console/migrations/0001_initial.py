# Generated by Django 2.2.4 on 2019-11-05 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CreateHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('database_name', models.CharField(max_length=100, unique=True)),
                ('collection_name', models.CharField(max_length=100, unique=True)),
                ('history', models.BooleanField(default=False, help_text='Check this to create a historical collection.\n                    When items are updated, the old data is saved in\n                    another collection')),
            ],
            options={
                'verbose_name_plural': 'Create Histories',
                'unique_together': {('database_name', 'collection_name')},
            },
        ),
    ]