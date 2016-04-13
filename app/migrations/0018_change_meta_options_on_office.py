# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_alter_fields_for_ldap_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='office',
            options={'ordering': ['name'], 'verbose_name': 'Secretar\xeda', 'verbose_name_plural': 'Secretar\xedas'},
        ),
    ]
