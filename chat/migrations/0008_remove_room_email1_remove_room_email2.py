# Generated by Django 4.2 on 2023-09-10 02:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_alter_room_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='email1',
        ),
        migrations.RemoveField(
            model_name='room',
            name='email2',
        ),
    ]