# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '10000_spamconfig_deactivate_spam_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpamScan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(blank=True)),
                ('modified', models.DateTimeField(blank=True)),
                ('website', models.CharField(max_length=255, null=True, blank=True)),
                ('started', models.DateTimeField(null=True, blank=True)),
                ('ended', models.DateTimeField(null=True, blank=True)),
                ('log', models.TextField(null=True, blank=True)),
                ('config', models.ForeignKey(to='web.SpamConfig')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='spamconfig',
            name='created',
            field=models.DateTimeField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spamconfig',
            name='deactivate_spam_user',
            field=models.BooleanField(default=False, help_text=b'If a post is identified as SPAM, should the corresponding user be deactivated (status=0)?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spamconfig',
            name='modified',
            field=models.DateTimeField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='systemconfig',
            name='created',
            field=models.DateTimeField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='systemconfig',
            name='modified',
            field=models.DateTimeField(blank=True),
            preserve_default=True,
        ),
    ]
