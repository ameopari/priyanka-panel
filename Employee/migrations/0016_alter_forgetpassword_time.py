# Generated by Django 3.2.9 on 2022-01-20 08:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0015_auto_20211210_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forgetpassword',
            name='time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 1, 20, 8, 14, 47, 290240)),
        ),
    ]
