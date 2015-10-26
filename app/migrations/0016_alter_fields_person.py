# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_add_field_person_ldap_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='person',
            name='surname',
            field=models.CharField(max_length=200, verbose_name='Apellido'),
        ),
    ]
