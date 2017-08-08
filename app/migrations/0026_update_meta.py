# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-08 13:58
from __future__ import unicode_literals

import app.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_update_fields_and_meta'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='office',
            options={'ordering': ['name'], 'verbose_name': 'Secretar\xeda', 'verbose_name_plural': 'Secretar\xedas'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Persona', 'verbose_name_plural': 'Personas'},
        ),
        migrations.AlterField(
            model_name='person',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creado'),
        ),
        migrations.AlterField(
            model_name='person',
            name='document_number',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(message='Ingrese un valor v\xe1lido', regex=b'^\\d{6,10}$')], verbose_name='N\xfamero Documento'),
        ),
        migrations.AlterField(
            model_name='person',
            name='document_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.DocumentType', verbose_name='Tipo Documento'),
        ),
        migrations.AlterField(
            model_name='person',
            name='group_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Grupo'),
        ),
        migrations.AlterField(
            model_name='person',
            name='ldap_user_name',
            field=models.CharField(blank=True, max_length=200, null=True, validators=[app.models.validate_ldap_user_name], verbose_name='Nombre de usuario ldap'),
        ),
        migrations.AlterField(
            model_name='person',
            name='received_application',
            field=models.BooleanField(default=False, verbose_name='Solicitud recibida'),
        ),
        migrations.AlterField(
            model_name='person',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='actualizado'),
        ),
    ]
