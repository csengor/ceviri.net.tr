# Generated by Django 4.0.3 on 2022-03-03 09:44

import app.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_segment_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranslationQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.JSONField()),
                ('secret', models.CharField(default=app.utils.generate_secret, max_length=8, unique=True)),
                ('status', models.IntegerField(choices=[(1, 'New'), (2, 'Processing'), (3, 'Ready')], default=1)),
            ],
        ),
    ]
