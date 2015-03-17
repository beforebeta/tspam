# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '10012_spamconfig_notification_recipients'),
    ]

    operations = [
        migrations.AddField(
            model_name='spamconfig',
            name='is_full_scan_needed',
            field=models.BooleanField(default=False, help_text=b'Should the scanner review the latest 20 pages of posts or should it do an entire scan of the site?'),
            preserve_default=True,
        ),
    ]
