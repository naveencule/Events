# Generated by Django 5.0.3 on 2024-11-29 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_notes_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='book_ticket',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]