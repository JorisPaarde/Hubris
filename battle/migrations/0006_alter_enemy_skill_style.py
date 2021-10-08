# Generated by Django 3.2.7 on 2021-10-04 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0005_remove_enemy_xp_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enemy',
            name='skill_style',
            field=models.CharField(choices=[('LN', 'Lightning'), ('FR', 'Fire'), ('GL', 'Golem'), ('DR', 'Drain'), ('IC', 'Ice'), ('HL', 'Heal')], max_length=2),
        ),
    ]