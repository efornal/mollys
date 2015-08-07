# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_updated_translations_forms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_id', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Group',
                'managed': False,
                'verbose_name_plural': 'Groups',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='group_id',
            field=models.IntegerField(null=True, verbose_name='group_id', blank=True),
        ),
    ]
