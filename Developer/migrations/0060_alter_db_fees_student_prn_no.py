# Generated by Django 4.1.7 on 2023-04-23 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0059_alter_customuser_student_prn_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='db_fees',
            name='student_prn_no',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
