# Generated by Django 2.2.9 on 2020-05-16 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_remove_movie_subgeneres'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='birth_date',
        ),
    ]