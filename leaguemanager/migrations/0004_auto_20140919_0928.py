# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('leaguemanager', '0003_auto_20140918_2048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='league',
        ),
        migrations.AddField(
            model_name='game',
            name='season',
            field=models.ForeignKey(default=0, to='leaguemanager.Season'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='date',
            field=models.DateField(default=datetime.date(2014, 9, 19)),
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_joined',
            field=models.DateField(default=datetime.date(2014, 9, 19)),
        ),
        migrations.AlterField(
            model_name='season',
            name='begin_date',
            field=models.DateField(default=datetime.date(2014, 9, 19)),
        ),
        migrations.AlterField(
            model_name='season',
            name='end_date',
            field=models.DateField(default=datetime.date(2014, 9, 19)),
        ),
    ]
