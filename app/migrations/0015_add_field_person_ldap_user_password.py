# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_verbose_name_for_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='ldap_user_password',
            field=models.CharField(max_length=200, null=True, verbose_name='Contrase\xf1a', blank=True),
        ),
    ]
