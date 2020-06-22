# Generated by Django 2.2.9 on 2020-05-16 16:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieScreenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='screenshots/')),
                ('create_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_moviescreenshot', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('score', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('summary', models.CharField(max_length=128)),
                ('body', models.TextField()),
                ('create_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_review', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='genere',
            name='description',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='description',
        ),
        migrations.AddField(
            model_name='movie',
            name='summary',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='portrait',
            field=models.ImageField(null=True, upload_to='portraits/'),
        ),
        migrations.DeleteModel(
            name='SubGenere',
        ),
        migrations.AddField(
            model_name='review',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='review',
            name='update_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_review', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='moviescreenshot',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screenshots', to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='moviescreenshot',
            name='update_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_moviescreenshot', to=settings.AUTH_USER_MODEL),
        ),
    ]