# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '10001_auto_20150109_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='spamconfig',
            name='spam_user_names',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
