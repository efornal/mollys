# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_add_received_application'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documenttype',
            options={'verbose_name': 'Tipo Documento', 'verbose_name_plural': 'Tipos de Documentos'},
        ),
        migrations.AlterModelOptions(
            name='office',
            options={'verbose_name': 'Secretar\xeda', 'verbose_name_plural': 'Secretar\xedas'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Persona', 'verbose_name_plural': 'Personas'},
        ),
        migrations.AlterField(
            model_name='office',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='person',
            name='address',
            field=models.CharField(max_length=200, null=True, verbose_name='Domicilio', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creado'),
        ),
        migrations.AlterField(
            model_name='person',
            name='document_number',
            field=models.CharField(max_length=200, verbose_name='N\xfamero Documento', validators=[django.core.validators.RegexValidator(regex=b'^\\d{6,10}$', message=b'Ingrese un valor v\xc3\xa1lido')]),
        ),
        migrations.AlterField(
            model_name='person',
            name='document_type',
            field=models.ForeignKey(verbose_name='Tipo Documento', to='app.DocumentType'),
        ),
        migrations.AlterField(
            model_name='person',
            name='home_phone',
            field=models.CharField(max_length=200, null=True, verbose_name='Tel\xe9fono particular', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='ldap_user_name',
            field=models.CharField(max_length=200, null=True, verbose_name='Nombre de usuario ldap', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nombres'),
        ),
        migrations.AlterField(
            model_name='person',
            name='office',
            field=models.ForeignKey(verbose_name='Secretar\xeda', blank=True, to='app.Office', null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='other_office',
            field=models.CharField(max_length=200, null=True, verbose_name='Otra Secretar\xeda', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='position',
            field=models.CharField(max_length=200, null=True, verbose_name='Cargo', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='received_application',
            field=models.BooleanField(default=False, verbose_name='Solicitud recibida'),
        ),
        migrations.AlterField(
            model_name='person',
            name='surname',
            field=models.CharField(max_length=200, verbose_name='Apellidos'),
        ),
        migrations.AlterField(
            model_name='person',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='actualizado'),
        ),
        migrations.AlterField(
            model_name='person',
            name='work_phone',
            field=models.CharField(max_length=200, null=True, verbose_name='Tel\xe9fono laboral', blank=True),
        ),
    ]
