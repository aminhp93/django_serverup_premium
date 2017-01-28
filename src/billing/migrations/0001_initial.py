# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 05:02
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateTimeField(default=datetime.datetime(2017, 1, 27, 5, 2, 9, 471184, tzinfo=utc), verbose_name='Start date')),
                ('date_end', models.DateTimeField(default=datetime.datetime(2017, 1, 27, 5, 2, 9, 471260, tzinfo=utc), verbose_name='End date')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]