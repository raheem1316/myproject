# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-03 07:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('queriesapp', '0004_auto_20171203_1239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='user',
            new_name='user_details',
        ),
    ]
