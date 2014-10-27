# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('leaguemanager', '0009_auto_20141026_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodBonus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.date(2014, 10, 26))),
                ('player', models.ForeignKey(to='leaguemanager.Player')),
                ('season', models.ForeignKey(to='leaguemanager.Season')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
