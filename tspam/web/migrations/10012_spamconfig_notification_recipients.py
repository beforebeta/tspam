# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '10011_auto_20150110_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='spamconfig',
            name='notification_recipients',
            field=models.TextField(help_text=b'Enter your email address here', null=True, blank=True),
            preserve_default=True,
        ),
    ]
