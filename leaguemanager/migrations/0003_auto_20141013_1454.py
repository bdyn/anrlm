# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('leaguemanager', '0002_auto_20140925_0942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodbonus',
            name='date',
        ),
        migrations.RemoveField(
            model_name='foodbonus',
            name='scorecard',
        ),
        migrations.RemoveField(
            model_name='player',
            name='user',
        ),
        migrations.RemoveField(
            model_name='scorecard',
            name='player',
        ),
        migrations.RemoveField(
            model_name='scorecard',
            name='season',
        ),
        migrations.AddField(
            model_name='player',
            name='email_address',
            field=models.CharField(default=b'email', max_length=128),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='first_name',
            field=models.CharField(default=b'first', max_length=128),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='last_name',
            field=models.CharField(default=b'last', max_length=128),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='name',
            field=models.CharField(default=b'handle', max_length=128),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='date',
            field=models.DateField(default=datetime.date(2014, 10, 13)),
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_joined',
            field=models.DateField(default=datetime.date(2014, 10, 13)),
        ),
        migrations.AlterField(
            model_name='season',
            name='begin_date',
            field=models.DateField(default=datetime.date(2014, 10, 13)),
        ),
        migrations.AlterField(
            model_name='season',
            name='end_date',
            field=models.DateField(default=datetime.date(2014, 11, 12)),
        ),
    ]
