# Generated by Django 3.1.1 on 2020-09-22 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lesson_scheduling', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subjects',
            new_name='Subject',
        ),
    ]