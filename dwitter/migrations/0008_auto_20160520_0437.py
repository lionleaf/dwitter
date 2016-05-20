# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0007_auto_20160519_0039'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-posted',)},
        ),
        migrations.AlterModelOptions(
            name='dweet',
            options={'ordering': ('-posted',)},
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='dweet',
            name='reply_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='dwitter.Dweet', null=True),
        ),
    ]
