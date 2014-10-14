# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaguemanager', '0005_delete_scorecard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='winner',
        ),
        migrations.AddField(
            model_name='game',
            name='outcome',
            field=models.CharField(default=b'draw', max_length=22, choices=[(b'draw', b'draw'), (b'corp agenda victory', b'corp agenda victory'), (b'runner agenda victory', b'runner agenda victory'), (b'flatline', b'flatline'), (b'mill', b'mill')]),
            preserve_default=True,
        ),
    ]
