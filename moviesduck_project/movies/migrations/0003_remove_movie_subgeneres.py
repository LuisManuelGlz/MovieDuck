# Generated by Django 2.2.9 on 2020-05-16 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20200516_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='subgeneres',
        ),
    ]
