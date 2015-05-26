# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_office'),
    ]

    operations = [
        migrations.RemoveField('person', 'office'),
        migrations.AddField(
            model_name='person',
            name='office',
            field=models.ForeignKey(blank=True, to='app.Office', null=True),
        ),
    ]
