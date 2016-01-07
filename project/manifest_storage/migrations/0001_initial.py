# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ManifestEntryModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('remote_name', models.CharField(max_length=255, null=True, blank=True)),
                ('buffer_name', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
    ]
