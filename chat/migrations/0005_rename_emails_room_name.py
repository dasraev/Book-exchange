# Generated by Django 4.2 on 2023-07-20 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_room_unique_together_room_emails_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='emails',
            new_name='name',
        ),
    ]