# Generated by Django 3.2.7 on 2021-10-12 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_alter_player_healing_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='drain_attack_phase',
            field=models.CharField(choices=[('1', 'I'), ('2', 'II'), ('3', 'III'), ('4', 'IV'), ('5', 'V'), ('ALL', 'I-V'), ('NONE', '')], default='ALL', max_length=4),
        ),
        migrations.AddField(
            model_name='player',
            name='fire_attack_phase',
            field=models.CharField(choices=[('1', 'I'), ('2', 'II'), ('3', 'III'), ('4', 'IV'), ('5', 'V'), ('ALL', 'I-V'), ('NONE', '')], default='2', max_length=4),
        ),
        migrations.AddField(
            model_name='player',
            name='golem_attack_phase',
            field=models.CharField(choices=[('1', 'I'), ('2', 'II'), ('3', 'III'), ('4', 'IV'), ('5', 'V'), ('ALL', 'I-V'), ('NONE', '')], default='4', max_length=4),
        ),
        migrations.AddField(
            model_name='player',
            name='ice_attack_phase',
            field=models.CharField(choices=[('1', 'I'), ('2', 'II'), ('3', 'III'), ('4', 'IV'), ('5', 'V'), ('ALL', 'I-V'), ('NONE', '')], default='3', max_length=4),
        ),
        migrations.AddField(
            model_name='player',
            name='lightning_attack_phase',
            field=models.CharField(choices=[('1', 'I'), ('2', 'II'), ('3', 'III'), ('4', 'IV'), ('5', 'V'), ('ALL', 'I-V'), ('NONE', '')], default='1', max_length=4),
        ),
    ]