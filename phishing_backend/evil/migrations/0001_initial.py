# Generated by Django 4.1.7 on 2023-09-14 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PhishingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('hash', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=200)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
    ]
