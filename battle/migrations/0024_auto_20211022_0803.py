# Generated by Django 3.2.7 on 2021-10-22 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0023_rename_max_health_game_floor_enemy_health_max'),
    ]

    operations = [
        migrations.AlterField(
            model_name='current_game_floor',
            name='current_phase',
            field=models.CharField(choices=[('1', 'I'), ('2', 'II'), ('3', 'III'), ('4', 'IV')], default='1', max_length=1),
        ),
        migrations.AlterField(
            model_name='game_floor_enemy',
            name='attack_phase',
            field=models.CharField(choices=[('1', 'I'), ('2', 'II'), ('3', 'III'), ('4', 'IV')], default='1', max_length=1),
        ),
    ]