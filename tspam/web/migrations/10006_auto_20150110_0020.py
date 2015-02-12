# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '10005_auto_20150110_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spampost',
            name='post_id',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
