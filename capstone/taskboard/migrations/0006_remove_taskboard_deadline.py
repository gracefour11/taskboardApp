# Generated by Django 3.1.5 on 2022-07-22 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskboard', '0005_auto_20220702_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskboard',
            name='deadline',
        ),
    ]
