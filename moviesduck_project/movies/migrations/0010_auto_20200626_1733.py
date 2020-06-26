# Generated by Django 2.2.9 on 2020-06-26 17:33

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0009_auto_20200624_0332'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('content_type', 'object_id', 'create_user')},
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('create_user', 'movie')},
        ),
    ]
