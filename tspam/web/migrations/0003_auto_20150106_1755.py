# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_spamconfig_last_complete_run'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spamconfig',
            old_name='spam_filter_fields',
            new_name='title_scan_spam_filter_fields',
        ),
        migrations.AddField(
            model_name='spamconfig',
            name='content_scan_spam_filter_fields',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
