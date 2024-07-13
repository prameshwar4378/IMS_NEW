# Generated by Django 4.1.7 on 2023-04-15 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0032_alter_customuser_academic_session'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='institute_profile',
        ),
        migrations.AddField(
            model_name='customuser',
            name='institute_logo',
            field=models.ImageField(blank=True, null=True, upload_to='institute_logo/'),
        ),
    ]
