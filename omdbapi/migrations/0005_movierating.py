# Generated by Django 3.0 on 2020-01-16 00:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('omdbapi', '0004_usermovielist'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='omdbapi.Movie')),
            ],
        ),
    ]
