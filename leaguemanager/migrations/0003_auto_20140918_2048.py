# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaguemanager', '0002_auto_20140918_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='winner',
            field=models.CharField(
                default=b'draw',
                max_length=8,
                choices=[(b'draw', b'draw'), (b'corp', b'corp'), (b'runner', b'runner')]),
        ),
    ]
