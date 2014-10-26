# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('leaguemanager', '0008_auto_20141024_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='corp_ID',
            field=models.CharField(default=b'none', max_length=128, choices=[(b'Cerebral Imaging: Infinite Frontiers', b'Cerebral Imaging: Infinite Frontiers'), (b'Chronos Protocol (Hass-Bioroid): Selective Mind-mapping', b'Chronos Protocol (Hass-Bioroid): Selective Mind-mapping'), (b'Custom Biotics: Engineered for Success', b'Custom Biotics: Engineered for Success'), (b'Hass-Bioroid: Engineering the Future', b'Hass-Bioroid: Engineering the Future'), (b'Hass-Bioroid: Stronger Together', b'Hass-Bioroid: Stronger Together'), (b'NEXT Design: Guarding the Net', b'NEXT Design: Guarding the Net'), (b'The Foundary: Refining the Process', b'The Foundary: Refining the Process'), (b'Chronos Protocol (Jinteki): Selective Mind-mapping', b'Chronos Protocol (Jinteki): Selective Mind-mapping'), (b'Jinteki: Personal Evolution', b'Jinteki: Personal Evolution'), (b'Jinteki: Replicating Perfection', b'Jinteki: Replicating Perfection'), (b'Nisei Division: The Next Generation', b'Nisei Division: The Next Generation'), (b'Tennin Institute: The Secrets Within', b'Tennin Institute: The Secrets Within'), (b'NBN: Making News', b'NBN: Making News'), (b'NBN: The World is Yours', b'NBN: The World is Yours'), (b'Near-Earth Hub: Broadcast Center', b'Near-Earth Hub: Broadcast Center'), (b'Blue Sun: Powering the Future', b'Blue Sun: Powering the Future'), (b'Gagarin Deep Space: Expanding the Horizon', b'Gagarin Deep Space: Expanding the Horizon'), (b'GRNDL: Power Unleashed', b'GRNDL: Power Unleashed'), (b'Weyland Consortium: Because We Built It', b'Weyland Consortium: Because We Built It'), (b'Weyland Consortium: Buidling a Better World', b'Weyland Consortium: Buidling a Better World'), (b'The Shadow: Pulling the Strings', b'The Shadow: Pulling the Strings'), (b'none', b'none')]),
        ),
        migrations.AlterField(
            model_name='game',
            name='date',
            field=models.DateField(default=datetime.date(2014, 10, 26)),
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_joined',
            field=models.DateField(default=datetime.date(2014, 10, 26)),
        ),
        migrations.AlterField(
            model_name='season',
            name='begin_date',
            field=models.DateField(default=datetime.date(2014, 10, 26)),
        ),
        migrations.AlterField(
            model_name='season',
            name='end_date',
            field=models.DateField(default=datetime.date(2014, 11, 25)),
        ),
    ]
