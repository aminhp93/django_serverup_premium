# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-22 17:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_remove_notification_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notification',
            name='unread',
            field=models.BooleanField(default=True),
        ),
    ]
