# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('winner', models.CharField(max_length=24)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_joined', models.DateField()),
                ('league', models.ForeignKey(to='leaguemanager.League')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('favorite_faction', models.CharField(max_length=128)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scorecard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('player', models.ForeignKey(to='leaguemanager.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('league', models.ForeignKey(to='leaguemanager.League')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='scorecard',
            name='season',
            field=models.ForeignKey(to='leaguemanager.Season'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membership',
            name='player',
            field=models.ForeignKey(to='leaguemanager.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='league',
            name='members',
            field=models.ManyToManyField(to='leaguemanager.Player', through='leaguemanager.Membership'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='league',
            name='organizer',
            field=models.OneToOneField(related_name=b'organizer', default=0, to='leaguemanager.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='corp_player',
            field=models.ForeignKey(related_name=b'corp_player', to='leaguemanager.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='league',
            field=models.ForeignKey(default=0, to='leaguemanager.League'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='runner_player',
            field=models.ForeignKey(related_name=b'runner_player', to='leaguemanager.Player'),
            preserve_default=True,
        ),
    ]
