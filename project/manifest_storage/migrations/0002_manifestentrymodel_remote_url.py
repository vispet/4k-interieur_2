# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manifest_storage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='manifestentrymodel',
            name='remote_url',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
