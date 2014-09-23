# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaguemanager', '0008_auto_20140922_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='favorite_faction',
            field=models.CharField(default=b'neutral', max_length=13),
        ),
    ]
