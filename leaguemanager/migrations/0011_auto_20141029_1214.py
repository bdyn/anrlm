# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('leaguemanager', '0010_foodbonus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodbonus',
            name='date',
            field=models.DateField(default=datetime.date(2014, 10, 29)),
        ),
        migrations.AlterField(
            model_name='game',
            name='date',
            field=models.DateField(default=datetime.date(2014, 10, 29), db_index=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_joined',
            field=models.DateField(default=datetime.date(2014, 10, 29)),
        ),
        migrations.AlterField(
            model_name='season',
            name='begin_date',
            field=models.DateField(default=datetime.date(2014, 10, 29)),
        ),
        migrations.AlterField(
            model_name='season',
            name='end_date',
            field=models.DateField(default=datetime.date(2014, 11, 28)),
        ),
        migrations.AlterIndexTogether(
            name='game',
            index_together=set([('corp_player', 'season')]),
        ),
    ]
