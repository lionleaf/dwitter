# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0011_auto_20160819_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='dweet',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dweet',
            name='reply_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='dwitter.Dweet', null=True),
        ),
    ]
