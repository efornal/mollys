# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-09 12:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_change_meta_options_on_office'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='alternative_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='alternative_email'),
        ),
        migrations.AddField(
            model_name='person',
            name='email',
            field=models.EmailField(blank=True, null=True, default=None, max_length=254, verbose_name='email'),
        ),
    ]
