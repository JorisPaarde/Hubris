# Generated by Django 3.2.7 on 2021-10-05 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0007_alter_current_game_floor_current_phase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='current_game_floor',
            name='Enemy',
        ),
        migrations.AddField(
            model_name='current_game_floor',
            name='Enemy',
            field=models.ManyToManyField(to='battle.Game_floor_enemy'),
        ),
    ]