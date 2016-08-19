# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0009_auto_20160816_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='dweet',
            name='hotscore',
            field=models.IntegerField(default=1),
        ),
    ]
