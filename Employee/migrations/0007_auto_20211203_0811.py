# Generated by Django 3.2.9 on 2021-12-03 08:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0006_auto_20211203_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forgetpassword',
            name='time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 12, 3, 8, 11, 24, 256294)),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_desc',
            field=models.TextField(max_length=30, null=True),
        ),
    ]