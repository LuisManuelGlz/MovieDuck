# Generated by Django 2.2.9 on 2020-03-01 23:36

from django.db import migrations, models
import registration.models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='profiles_pics/default.jpg', upload_to=registration.models.custom_upload_to),
        ),
    ]
