# Generated by Django 4.2 on 2023-07-19 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_remove_room_name_remove_room_slug_room_email1_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='room',
            unique_together={('email1', 'email2')},
        ),
    ]
