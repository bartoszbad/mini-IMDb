# Generated by Django 3.0 on 2020-01-16 03:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('omdbapi', '0006_auto_20200116_0222'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieOnList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='omdbapi.UserMovieList')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='omdbapi.Movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]