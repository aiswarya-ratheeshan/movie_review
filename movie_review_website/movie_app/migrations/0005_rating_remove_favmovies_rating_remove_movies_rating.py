# Generated by Django 4.2.11 on 2024-03-17 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0004_remove_review_rating_favmovies_rating_movies_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=250)),
                ('movie', models.CharField(max_length=250)),
                ('rating', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='favmovies',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='movies',
            name='rating',
        ),
    ]
