# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_position_not_required'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='document_number',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(regex=b'^\\d{6,10}$', message=b'Ingrese un valor v\xc3\xa1lido')]),
        ),
    ]
