# Generated by Django 2.0.3 on 2018-05-13 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_mission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Character'),
        ),
    ]