# Generated by Django 3.2.7 on 2021-10-04 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_alter_card_skill_style'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='healing_attack_cost',
            new_name='healing_cost',
        ),
    ]
