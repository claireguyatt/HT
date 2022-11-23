# Generated by Django 4.1.2 on 2022-11-21 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('edit_variables', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('username', models.CharField(help_text='Enter your username here', max_length=20)),
                ('email', models.EmailField(help_text='Enter your email here', max_length=254)),
                ('number', models.CharField(help_text='Enter your phone number here', max_length=11)),
                ('gender', models.CharField(choices=[('Female', 'Female'), ('Male', 'Male'), ('Nonbinary', 'Nonbinary'), ('Other', 'Other')], default='Female', max_length=20)),
                ('dob', models.DateField()),
                ('data', models.JSONField(default=dict)),
                ('variables', models.ManyToManyField(related_name='users', to='edit_variables.variable')),
            ],
        ),
    ]