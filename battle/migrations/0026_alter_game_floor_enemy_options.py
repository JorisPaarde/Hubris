# Generated by Django 3.2.7 on 2021-10-26 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0025_auto_20211023_2157'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game_floor_enemy',
            options={'ordering': ['pk']},
        ),
    ]
