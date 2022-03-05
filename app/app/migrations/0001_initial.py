# Generated by Django 4.0.3 on 2022-03-02 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_language', models.CharField(choices=[('en', 'English'), ('tr', 'Turkish')], max_length=5)),
                ('target_language', models.CharField(choices=[('en', 'English'), ('tr', 'Turkish')], max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('miscellaneous', models.TextField(blank=True)),
                ('source_file', models.FileField(blank=True, upload_to='app/files/')),
                ('bilingual_file', models.FileField(upload_to='app/files/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_language', models.CharField(choices=[('en', 'English'), ('tr', 'Turkish')], max_length=5)),
                ('target_language', models.CharField(choices=[('en', 'English'), ('tr', 'Turkish')], max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('miscellaneous', models.TextField(blank=True)),
                ('source_segment', models.TextField()),
                ('reviewed_source_segment', models.TextField(blank=True)),
                ('target_segment', models.TextField(blank=True)),
                ('reviewed_target_segment', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
