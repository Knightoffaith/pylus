# Generated by Django 2.0.3 on 2018-06-07 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0020_auto_20180603_0505'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='character',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.Character'),
        ),
    ]
