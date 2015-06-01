# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_document_number_validations'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='other_office',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
