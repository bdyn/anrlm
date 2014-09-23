# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaguemanager', '0009_auto_20140922_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='favorite_faction',
            field=models.CharField(default=b'neutral', max_length=13, choices=[(b'neutral', b'neutral'), (b'anarch', b'anarch'), (b'criminal', b'criminal'), (b'shaper', b'shaper'), (b'hass-bioroid', b'hass-bioroid'), (b'jinteki', b'jinteki'), (b'nbn', b'nbn'), (b'weyland', b'weyland')]),
        ),
    ]
