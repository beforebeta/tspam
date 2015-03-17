# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '10004_auto_20150109_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpamPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(blank=True)),
                ('modified', models.DateTimeField(blank=True)),
                ('post_id', models.IntegerField(null=True, blank=True)),
                ('post_title', models.IntegerField(null=True, blank=True)),
                ('post_text', models.TextField(null=True, blank=True)),
                ('status', models.CharField(default=b'identified', max_length=20)),
                ('post_user', models.CharField(max_length=255, null=True, blank=True)),
                ('config', models.ForeignKey(to='web.SpamConfig')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='spamposts',
            name='config',
        ),
        migrations.DeleteModel(
            name='SpamPosts',
        ),
    ]
