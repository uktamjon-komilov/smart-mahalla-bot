# Generated by Django 3.2 on 2022-02-21 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_sector_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helperinfographic',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Media Fayl'),
        ),
        migrations.AlterField(
            model_name='leaderinfographic',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Media Fayl'),
        ),
    ]
