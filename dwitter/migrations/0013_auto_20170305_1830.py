# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import dwitter.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dwitter', '0012_auto_20170228_2305'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='_author',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='dweet',
            old_name='_author',
            new_name='author',
        ),
        migrations.AlterField(
            model_name='dweet',
            name='author',
            field=models.ForeignKey(on_delete=models.SET(dwitter.models.get_sentinel_user), blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
