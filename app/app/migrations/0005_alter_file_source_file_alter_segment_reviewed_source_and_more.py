# Generated by Django 4.0.3 on 2022-03-04 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_translationquery_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='source_file',
            field=models.FileField(blank=True, null=True, upload_to='app/files/'),
        ),
        migrations.AlterField(
            model_name='segment',
            name='reviewed_source',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='segment',
            name='reviewed_target',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='segment',
            name='target',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='segment',
            name='user_edited_target',
            field=models.TextField(blank=True, null=True),
        ),
    ]
