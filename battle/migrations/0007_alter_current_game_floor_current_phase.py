# Generated by Django 3.2.7 on 2021-10-04 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0006_alter_enemy_skill_style'),
    ]

    operations = [
        migrations.AlterField(
            model_name='current_game_floor',
            name='current_phase',
            field=models.CharField(choices=[('1', 'I'), ('2', 'II'), ('3', 'III'), ('4', 'IV'), ('5', 'V')], default='1', max_length=1),
        ),
    ]
