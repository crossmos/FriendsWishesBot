# Generated by Django 4.2 on 2025-01-06 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='telegram_id',
            field=models.IntegerField(unique=True),
        ),
    ]
