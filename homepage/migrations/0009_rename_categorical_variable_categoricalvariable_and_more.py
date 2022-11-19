# Generated by Django 4.1.2 on 2022-11-16 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0008_alter_categorical_variable_choices'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categorical_Variable',
            new_name='CategoricalVariable',
        ),
        migrations.AlterField(
            model_name='profile',
            name='variables',
            field=models.ManyToManyField(related_name='users', to='homepage.variable'),
        ),
    ]
