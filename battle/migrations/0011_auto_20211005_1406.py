# Generated by Django 3.2.7 on 2021-10-05 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0010_rename_enemy_current_game_floor_enemy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='current_game_floor',
            name='enemy',
        ),
        migrations.AddField(
            model_name='current_game_floor',
            name='enemy',
            field=models.ManyToManyField(to='battle.Game_floor_enemy'),
        ),
    ]