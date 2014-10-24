# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('leaguemanager', '0007_auto_20141019_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='corp_ID',
            field=models.CharField(default=b'none', max_length=128, choices=[(b'Cerebral Imaging: Infinite Frontiers', b'HB Cerebral Imaging: Infinite Frontiers'), (b'Chronos Protocol (Hass-Bioroid): Selective Mind-mapping', b'Chronos Protocol (Hass-Bioroid): Selective Mind-mapping'), (b'Custom Biotics: Engineered for Success', b'Custom Biotics: Engineered for Success'), (b'Hass-Bioroid: Engineering the Future', b'Hass-Bioroid: Engineering the Future'), (b'Hass-Bioroid: Stronger Together', b'Hass-Bioroid: Stronger Together'), (b'NEXT Design: Guarding the Net', b'NEXT Design: Guarding the Net'), (b'The Foundary: Refining the Process', b'The Foundary: Refining the Process'), (b'Chronos Protocol (Jinteki): Selective Mind-mapping', b'Chronos Protocol (Jinteki): Selective Mind-mapping'), (b'Jinteki: Personal Evolution', b'Jinteki: Personal Evolution'), (b'Jinteki: Replicating Perfection', b'Jinteki: Replicating Perfection'), (b'Nisei Division: The Next Generation', b'Nisei Division: The Next Generation'), (b'Tennin Institute: The Secrets Within', b'Tennin Institute: The Secrets Within'), (b'NBN: Making News', b'NBN: Making News'), (b'NBN: The World is Yours', b'NBN: The World is Yours'), (b'Near-Earth Hub: Broadcast Center', b'Near-Earth Hub: Broadcast Center'), (b'Blue Sun: Powering the Future', b'Blue Sun: Powering the Future'), (b'Gagarin Deep Space: Expanding the Horizon', b'Gagarin Deep Space: Expanding the Horizon'), (b'GRNDL: Power Unleashed', b'GRNDL: Power Unleashed'), (b'Weyland Consortium: Because We Built It', b'Weyland Consortium: Because We Built It'), (b'Weyland Consortium: Buidling a Better World', b'Weyland Consortium: Buidling a Better World'), (b'The Shadow: Pulling the Strings', b'The Shadow: Pulling the Strings'), (b'none', b'none')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='runner_ID',
            field=models.CharField(default=b'none', max_length=128, choices=[(b'Edward Kim: Humanitys Hammer', b'Edward Kim: Humanitys Hammer'), (b'Noise: Hacker Extraordinaire', b'Noise: Hacker Extraordinaire'), (b'Quetzal: Free Spirit', b'Quetzal: Free Spirit'), (b'Reina Roja: Freedom Fighter', b'Reina Roja: Freedom Fighter'), (b'Whizzard: Master Gamer', b'Whizzard: Master Gamer'), (b'Andromeda: Dispossessed Ristie', b'Andromeda: Dispossessed Ristie'), (b'Gabriel Santiago: Consummate Professional', b'Gabriel Santiago: Consummate Professional'), (b'Iain Stirling: Retired Spook', b'Iain Stirling: Retired Spook'), (b'Ken Express Tenma: Disappeared Clone', b'Ken Express Tenma: Disappeared Clone'), (b'Laramy Fisk: Savvy Investor', b'Laramy Fisk: Savvy Investor'), (b'Leela Patel: Trained Pragmatist', b'Leela Patel: Trained Pragmatist'), (b'Silhouette: Stealth Operative', b'Silhouette: Stealth Operative'), (b'Chaos Theory: Wunderkind', b'Chaos Theory: Wunderkind'), (b'Exile: Streethawk', b'Exile: Streethawk'), (b'Kate Mac McCaffrey: Digital Tinker', b'Kate Mac McCaffrey: Digital Tinker'), (b'Nasir Meidan: Cyber Explorer', b'Nasir Meidan: Cyber Explorer'), (b'Rielle Kit Peddler: Transhuman', b'Rielle Kit Peddler: Transhuman'), (b'The Collective: Williams, Wu, et al.', b'The Collective: Williams, Wu, et al.'), (b'The Professor: Keeper of Knowledge', b'The Professor: Keeper of Knowledge'), (b'The Masque: Cyber General', b'The Masque: Cyber General'), (b'none', b'none')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='date',
            field=models.DateField(default=datetime.date(2014, 10, 24)),
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_joined',
            field=models.DateField(default=datetime.date(2014, 10, 24)),
        ),
        migrations.AlterField(
            model_name='season',
            name='begin_date',
            field=models.DateField(default=datetime.date(2014, 10, 24)),
        ),
        migrations.AlterField(
            model_name='season',
            name='end_date',
            field=models.DateField(default=datetime.date(2014, 11, 23)),
        ),
    ]
