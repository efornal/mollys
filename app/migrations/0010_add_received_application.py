# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_add_ldap_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='received_application',
            field=models.BooleanField(default=False),
        ),
    ]
