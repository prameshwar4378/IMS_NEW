# Generated by Django 4.1.7 on 2023-04-07 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0013_rename_subject_class_db_subjects_class_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=255, null=True),
        ),
    ]
