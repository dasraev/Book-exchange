# Generated by Django 4.2 on 2023-05-07 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_alter_book_condition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='condition',
            field=models.CharField(blank=True, choices=[('N', 'New'), ('G', 'Good '), ('E', 'Excellent'), ('S', 'Satisfactory')], max_length=1),
        ),
    ]
