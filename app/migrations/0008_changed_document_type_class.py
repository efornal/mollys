# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_document_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='document_type',
            field=models.ForeignKey(to='app.DocumentType'),
        ),
    ]
