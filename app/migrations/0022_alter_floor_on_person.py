# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-11 11:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_add_floor_and_area_to_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='floor',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='piso'),
        ),
    ]
