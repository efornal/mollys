# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_fields_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='ldap_user_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre de usuario ldap', validators=[app.models.validate_ldap_user_name]),
        ),
        migrations.AlterField(
            model_name='person',
            name='ldap_user_password',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Contrase\xf1a', validators=[app.models.validate_ldap_user_password]),
        ),
    ]
