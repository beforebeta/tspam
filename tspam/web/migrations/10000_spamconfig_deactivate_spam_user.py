# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '9999_initial_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='spamconfig',
            name='deactivate_spam_user',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
