# Generated by Django 3.2.7 on 2021-10-15 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_auto_20211012_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.player_type'),
        ),
    ]
