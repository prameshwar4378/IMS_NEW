# Generated by Django 4.1.7 on 2023-04-25 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0061_customuser_institute_is_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='tour_is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
