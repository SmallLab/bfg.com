# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-05-13 12:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainbfg', '0007_auto_20170511_2132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='fb_id',
            new_name='facebook_id',
        ),
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
