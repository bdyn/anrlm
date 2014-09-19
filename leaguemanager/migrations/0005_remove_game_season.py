# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaguemanager', '0004_auto_20140919_0928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='season',
        ),
    ]
