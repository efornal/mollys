# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-31 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_alter_fields_ldap_user_name_and_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='office',
            name='enable',
            field=models.BooleanField(default=True, verbose_name='enable'),
        ),
    ]
