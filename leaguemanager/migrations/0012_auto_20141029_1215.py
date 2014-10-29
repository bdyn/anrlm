# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaguemanager', '0011_auto_20141029_1214'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='game',
            index_together=set([('corp_player', 'season'), ('runner_player', 'season')]),
        ),
    ]
