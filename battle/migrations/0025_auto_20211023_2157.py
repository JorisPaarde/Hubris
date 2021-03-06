# Generated by Django 3.2.7 on 2021-10-23 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0024_auto_20211022_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='current_game_floor',
            name='current_phase',
            field=models.CharField(choices=[('1', 'I'), ('2', 'II'), ('3', 'III'), ('4', 'IV'), ('5', 'V')], default='1', max_length=1),
        ),
        migrations.AlterField(
            model_name='game',
            name='current_game_floor',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='battle.current_game_floor'),
        ),
        migrations.AlterField(
            model_name='game_floor_enemy',
            name='attack_phase',
            field=models.CharField(choices=[('1', 'I'), ('2', 'II'), ('3', 'III'), ('4', 'IV'), ('5', 'V')], default='1', max_length=1),
        ),
        migrations.AlterField(
            model_name='game_floor_enemy',
            name='skill_style',
            field=models.CharField(choices=[('LN', 'Lightning'), ('FR', 'Fire'), ('GL', 'Golem'), ('DR', 'Drain'), ('IC', 'Ice'), ('HL', 'Heal'), ('MN', 'Mana')], default='LN', max_length=2),
        ),
    ]
