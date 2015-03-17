# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '10009_spampost_post_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spampost',
            name='post_content',
        ),
    ]
