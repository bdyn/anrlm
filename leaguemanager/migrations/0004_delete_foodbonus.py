# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaguemanager', '0003_auto_20141013_1454'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FoodBonus',
        ),
    ]
