# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaguemanager', '0005_remove_game_season'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='season',
            field=models.ForeignKey(default=0, to='leaguemanager.Season'),
            preserve_default=True,
        ),
    ]
