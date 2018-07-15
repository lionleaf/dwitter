# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from django.db import migrations, models

def add_hashtags(apps, schema_editor):
    Comment = apps.get_model("dwitter", "Comment")
    Hashtag = apps.get_model("dwitter", "Hashtag")
    for comment in Comment.objects.all():
        hash_pattern = re.compile(r'#(?P<hashtag>[_a-zA-Z\d]+)')
        for hashtag in re.findall(hash_pattern, comment.text):
            h = Hashtag.objects.get_or_create(name=hashtag.lower())[0]
            if not h.dweets.filter(id=comment.reply_to.id).exists():
                h.dweets.add(comment.reply_to)

class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0016_auto_20180407_2218'),
    ]

    operations = [
            migrations.RunPython(add_hashtags),
    ]
