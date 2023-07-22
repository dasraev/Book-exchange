# Generated by Django 4.2 on 2023-07-18 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='name',
        ),
        migrations.RemoveField(
            model_name='room',
            name='slug',
        ),
        migrations.AddField(
            model_name='room',
            name='email1',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='room',
            name='email2',
            field=models.EmailField(default='', max_length=254),
        ),
    ]
