# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-31 08:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsitem',
            name='image',
            field=models.ImageField(height_field=b'height', upload_to=b'article/teasers', width_field=b'width'),
        ),
    ]