# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0008_auto_20160520_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dweet',
            name='code',
            field=models.TextField(),
        ),
    ]
