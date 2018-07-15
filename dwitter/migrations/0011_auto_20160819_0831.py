# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0010_dweet_hotscore'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dweet',
            name='hotscore',
        ),
        migrations.AddField(
            model_name='dweet',
            name='hotness',
            field=models.FloatField(default=1.0),
        ),
    ]
