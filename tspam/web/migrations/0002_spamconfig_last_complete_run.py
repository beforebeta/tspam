# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='spamconfig',
            name='last_complete_run',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
