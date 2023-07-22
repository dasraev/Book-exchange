# Generated by Django 4.2 on 2023-07-21 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_rename_emails_room_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='email1',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='email2',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]