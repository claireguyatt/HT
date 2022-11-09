# Generated by Django 4.1.2 on 2022-11-09 15:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('prompt', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Categorical_Variable',
            fields=[
                ('variable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='homepage.variable')),
                ('is_binary', models.BooleanField()),
                ('choices', models.JSONField()),
            ],
            bases=('homepage.variable',),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('username', models.CharField(help_text='Enter your username here', max_length=20)),
                ('email', models.EmailField(help_text='Enter your email here', max_length=254)),
                ('number', models.CharField(help_text='Enter your phone number here', max_length=11)),
                ('gender', models.CharField(choices=[('Female', 'Female'), ('Male', 'Male'), ('Nonbinary', 'Nonbinary'), ('Other', 'Other')], default='Female', max_length=20)),
                ('dob', models.DateField()),
                ('variables', models.ManyToManyField(to='homepage.variable')),
            ],
        ),
    ]
