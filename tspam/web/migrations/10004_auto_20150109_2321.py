# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '10003_spamposts'),
    ]

    operations = [
        migrations.AddField(
            model_name='spamconfig',
            name='admin_password',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='spamconfig',
            name='admin_user',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spamconfig',
            name='website',
            field=models.CharField(help_text=b'Expected format is www.website_name.com. Example: www.finehomebuilding.com', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
