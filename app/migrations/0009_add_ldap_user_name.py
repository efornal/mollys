# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_changed_document_type_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='ldap_user_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
