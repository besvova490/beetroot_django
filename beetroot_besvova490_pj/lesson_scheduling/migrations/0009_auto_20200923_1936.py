# Generated by Django 3.1.1 on 2020-09-23 19:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lesson_scheduling', '0008_auto_20200923_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduling',
            name='lesson_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 23, 19, 36, 34, 640704, tzinfo=utc)),
        ),
    ]
