# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 05:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_membership'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='user',
        ),
        migrations.DeleteModel(
            name='Membership',
        ),
    ]