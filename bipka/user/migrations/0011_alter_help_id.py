# Generated by Django 4.2.3 on 2023-07-26 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_help_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='help',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
