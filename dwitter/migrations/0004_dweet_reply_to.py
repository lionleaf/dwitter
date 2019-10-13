# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0003_dweet_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='dweet',
            name='reply_to',
            field=models.ForeignKey(blank=True, to='dwitter.Dweet', null=True, on_delete=models.DO_NOTHING),
        ),
    ]
