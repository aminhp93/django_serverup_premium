# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 02:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pageview',
            name='timestamp',
            field=models.DateField(default=datetime.datetime(2017, 1, 27, 2, 0, 13, 432202, tzinfo=utc)),
        ),
    ]
