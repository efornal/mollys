# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('surname', models.CharField(max_length=200)),
                ('document_number', models.CharField(max_length=200)),
                ('document_type', models.IntegerField()),
                ('position', models.CharField(max_length=200, null=True)),
                ('office', models.CharField(max_length=200, null=True)),
                ('work_phone', models.CharField(max_length=200, null=True)),
                ('home_phone', models.CharField(max_length=200, null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'people',
                'verbose_name_plural': 'People',
            },
        ),
    ]
