# Generated by Django 2.2.9 on 2020-05-27 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_auto_20200526_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
    ]
