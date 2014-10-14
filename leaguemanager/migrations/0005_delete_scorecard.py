# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaguemanager', '0004_delete_foodbonus'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Scorecard',
        ),
    ]
