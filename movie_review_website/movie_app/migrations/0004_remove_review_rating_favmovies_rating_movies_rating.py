# Generated by Django 4.2.11 on 2024-03-17 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0003_review_rating_alter_review_date_alter_review_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='rating',
        ),
        migrations.AddField(
            model_name='favmovies',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='movies',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
