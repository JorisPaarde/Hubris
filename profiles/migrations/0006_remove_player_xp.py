# Generated by Django 3.2.7 on 2021-09-28 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_rename_hand_hand_card'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='xp',
        ),
    ]