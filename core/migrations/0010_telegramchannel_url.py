# Generated by Django 3.2 on 2022-02-16 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_telegramchannel'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramchannel',
            name='url',
            field=models.TextField(default=''),
        ),
    ]
