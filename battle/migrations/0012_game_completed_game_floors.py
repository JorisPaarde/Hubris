# Generated by Django 3.2.7 on 2021-10-08 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0011_auto_20211005_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='completed_game_floors',
            field=models.IntegerField(default=0),
        ),
    ]
