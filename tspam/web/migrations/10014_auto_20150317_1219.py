# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '10013_spamconfig_is_full_scan_needed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spamconfig',
            name='notification_recipients',
            field=models.TextField(help_text=b'Enter your email address here if you wish to be notified when new spam is found', null=True, blank=True),
            preserve_default=True,
        ),
    ]
