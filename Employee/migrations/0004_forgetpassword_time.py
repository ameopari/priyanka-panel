# Generated by Django 3.2.9 on 2021-11-30 13:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0003_auto_20211130_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='forgetpassword',
            name='time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 30, 13, 23, 42, 387548)),
        ),
    ]