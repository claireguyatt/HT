# Generated by Django 4.1.2 on 2023-05-04 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='analysis',
            field=models.TextField(default='x'),
            preserve_default=False,
        ),
    ]