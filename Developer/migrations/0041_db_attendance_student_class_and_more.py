# Generated by Django 4.1.7 on 2023-04-17 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0040_alter_db_attendance_student_prn_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_attendance',
            name='student_class',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='db_attendance',
            name='student_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='db_attendance',
            name='attendance_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='db_attendance',
            name='student_prn_no',
            field=models.CharField(max_length=50, null=True),
        ),
    ]