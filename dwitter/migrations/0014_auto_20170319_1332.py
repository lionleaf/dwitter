# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0013_auto_20170305_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dweet',
            name='hotness',
            field=models.FloatField(default=1.0, db_index=True),
        ),
        migrations.AlterField(
            model_name='dweet',
            name='posted',
            field=models.DateTimeField(db_index=True),
        ),
    ]
