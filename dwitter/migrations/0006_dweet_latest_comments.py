# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='dweet',
            name='latest_comments',
            field=models.ManyToManyField(to='dwitter.Comment'),
        ),
    ]
