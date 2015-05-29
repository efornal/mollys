# -*- coding: utf-8 -*-
# FIXME
# convert postgres raw query to django migration

from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_office_relationship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='position',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.RunSQL('ALTER TABLE people ALTER COLUMN position DROP NOT NULL',
                          'ALTER TABLE people ALTER COLUMN position SET NOT NULL'),
        migrations.RunSQL('ALTER TABLE people ALTER COLUMN position SET DEFAULT NULL',
                          'ALTER TABLE people ALTER COLUMN position DROP DEFAULT'),
    ]
