# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0006_dweet_latest_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dweet',
            name='latest_comments',
        ),
        migrations.AlterField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(related_name='comments', to='dwitter.Dweet', on_delete=models.DO_NOTHING),
        ),
    ]
