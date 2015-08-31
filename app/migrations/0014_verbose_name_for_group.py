# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_added_ldap_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'managed': False, 'verbose_name': 'Grupo', 'verbose_name_plural': 'Grupos'},
        ),
        migrations.AlterField(
            model_name='person',
            name='group_id',
            field=models.IntegerField(null=True, verbose_name='Grupo', blank=True),
        ),
    ]
