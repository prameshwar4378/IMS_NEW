# Generated by Django 4.1.7 on 2023-04-09 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0018_db_result_percentage_db_result_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='db_result',
            name='class_name',
        ),
        migrations.RemoveField(
            model_name='db_result',
            name='student_name',
        ),
    ]