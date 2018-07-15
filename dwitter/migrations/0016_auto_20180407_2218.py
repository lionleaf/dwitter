# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0015_hashtag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtag',
            name='dweets',
            field=models.ManyToManyField(related_name='hashtag', to='dwitter.Dweet', blank=True),
        ),
        migrations.AlterField(
            model_name='hashtag',
            name='name',
            field=models.CharField(unique=True, max_length=30, db_index=True),
        ),
    ]
