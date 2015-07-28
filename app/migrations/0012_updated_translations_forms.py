# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_updated_translations_models'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='document_number',
            field=models.CharField(max_length=200, verbose_name='N\xfamero Documento', validators=[django.core.validators.RegexValidator(regex=b'^\\d{6,10}$', message='Ingrese un valor v\xe1lido')]),
        ),
    ]
