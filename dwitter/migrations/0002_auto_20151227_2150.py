# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-27 21:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dweet',
            old_name='owner',
            new_name='author',
        ),
    ]
