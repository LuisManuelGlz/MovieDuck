# Generated by Django 2.2.9 on 2020-03-01 23:54

from django.db import migrations, models
import registration.models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20200301_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='default.jpg', upload_to=registration.models.custom_upload_to),
        ),
    ]
