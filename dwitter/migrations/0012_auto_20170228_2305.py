# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dwitter', '0011_auto_20160819_0831'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='author',
            new_name='_author',
        ),
        migrations.RenameField(
            model_name='dweet',
            old_name='author',
            new_name='_author',
        ),
        migrations.AlterField(
            model_name='dweet',
            name='_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
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
