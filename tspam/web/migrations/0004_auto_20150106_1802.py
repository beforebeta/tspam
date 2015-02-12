# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20150106_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(editable=False, blank=True)),
                ('modified', models.DateTimeField(editable=False, blank=True)),
                ('stopwords_list', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='spamconfig',
            name='content_scan_spam_filter_fields',
            field=models.TextField(help_text=b"Use this section to specify the terms that should be checked in the body of the posting. Be VERY CAREFUL with the terms you enter here. If a posting's content contains any of the terms in this list, it will be deleted. When in doubt, ignore this section.", null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='spamconfig',
            name='title_scan_spam_filter_fields',
            field=models.TextField(help_text=b"Use this section to specify the terms that should be checked in the title of the posting. If a posting's title contains any of the terms in this list, it will be deleted.", null=True, blank=True),
            preserve_default=True,
        ),
    ]
