# Generated by Django 4.2.11 on 2024-03-17 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0005_rating_remove_favmovies_rating_remove_movies_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
