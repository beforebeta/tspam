# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '10008_spampost_post_user_edit'),
    ]

    operations = [
        migrations.AddField(
            model_name='spampost',
            name='post_content',
            field=picklefield.fields.PickledObjectField(null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
