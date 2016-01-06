# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dwitter', '0002_auto_20151227_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='dweet',
            name='likes',
            field=models.ManyToManyField(related_name='liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
