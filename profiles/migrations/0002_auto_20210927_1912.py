# Generated by Django 3.2.7 on 2021-09-27 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='hand',
            field=models.ManyToManyField(to='profiles.Card'),
        ),
        migrations.DeleteModel(
            name='Hand_card',
        ),
    ]
