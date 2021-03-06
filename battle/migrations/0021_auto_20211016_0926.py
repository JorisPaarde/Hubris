# Generated by Django 3.2.7 on 2021-10-16 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0020_alter_game_current_game_floor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='completed_game_floors',
            new_name='current_game_floor_number',
        ),
        migrations.AddField(
            model_name='game',
            name='total_gamefloors_played',
            field=models.IntegerField(default=0),
        ),
    ]
