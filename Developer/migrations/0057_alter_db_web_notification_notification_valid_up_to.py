# Generated by Django 4.1.7 on 2023-04-22 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0056_db_web_notification_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='db_web_notification',
            name='notification_valid_up_to',
            field=models.DateField(blank=True, null=True),
        ),
    ]