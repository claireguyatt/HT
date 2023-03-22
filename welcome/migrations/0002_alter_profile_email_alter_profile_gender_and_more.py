# Generated by Django 4.1.2 on 2023-03-22 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(help_text='Required. Enter your email.', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('Woman', 'Woman'), ('Man', 'Man'), ('Non binary', 'Non binary'), ('Other', 'Other')], default='Woman', max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='number',
            field=models.CharField(help_text='Enter your phone number.', max_length=11),
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(max_length=150),
        ),
    ]