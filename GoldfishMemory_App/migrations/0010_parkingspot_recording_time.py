# Generated by Django 3.2 on 2022-02-09 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoldfishMemory_App', '0009_alter_parkingspot_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkingspot',
            name='recording_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
