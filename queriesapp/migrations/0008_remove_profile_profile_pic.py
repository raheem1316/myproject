# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-03 10:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('queriesapp', '0007_auto_20171203_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_pic',
        ),
    ]
