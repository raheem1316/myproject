# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-03 11:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queriesapp', '0012_auto_20171203_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images'),
        ),
    ]
