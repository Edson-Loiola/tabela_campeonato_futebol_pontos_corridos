# Generated by Django 5.0.4 on 2024-05-23 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabela', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='team_away',
            new_name='away_team',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='team_home',
            new_name='home_team',
        ),
        migrations.RemoveField(
            model_name='match',
            name='date',
        ),
        migrations.AddField(
            model_name='match',
            name='played',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='match',
            name='away_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='match',
            name='home_score',
            field=models.IntegerField(default=0),
        ),
    ]