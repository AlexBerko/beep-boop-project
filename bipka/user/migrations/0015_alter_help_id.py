# Generated by Django 4.2.3 on 2023-07-26 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_alter_help_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='help',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
