# Generated by Django 3.1.5 on 2022-07-23 07:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taskboard', '0007_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=50)),
                ('description', models.CharField(default=None, max_length=200)),
                ('deadline', models.DateField(default=None, null=True)),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('last_modified_dt', models.DateTimeField(auto_now=True)),
                ('delete_ind', models.CharField(default='F', max_length=1)),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asignee', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Task_created_by', to=settings.AUTH_USER_MODEL)),
                ('last_modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Task_last_modified_by', to=settings.AUTH_USER_MODEL)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sectionForTask', related_query_name='sectionForTask', to='taskboard.section')),
                ('taskboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taskboardForTask', related_query_name='taskboardForTask', to='taskboard.taskboard')),
            ],
        ),
    ]
