# Generated by Django 4.1.7 on 2023-04-09 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0014_customuser_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='DB_Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(choices=[('1st Standerd', '1st Standerd'), ('2nd Standerd', '2nd Standerd'), ('3rd Standerd', '3rd Standerd'), ('4th Standerd', '4th Standerd'), ('6th Standerd', '6th Standerd'), ('7th Standerd', '7th Standerd'), ('8th Standerd', '8th Standerd'), ('9th Standerd', '9th Standerd'), ('10th Standerd', '10th Standerd'), ('11th Standerd', '11th Standerd'), ('12th Standerd', '12th Standerd')], max_length=50, null=True)),
                ('student_name', models.CharField(max_length=100, null=True)),
                ('student_prn_no', models.CharField(max_length=100, null=True)),
                ('subject_name', models.CharField(max_length=100, null=True)),
                ('min_marks', models.CharField(max_length=100, null=True)),
                ('obtained_marks', models.CharField(max_length=100, null=True)),
                ('passing_marks', models.CharField(max_length=100, null=True)),
                ('out_off_marks', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='db_subjects',
            name='min_marks',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='db_subjects',
            name='obtained_marks',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='db_subjects',
            name='out_off_marks',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='db_subjects',
            name='passing_marks',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='db_subjects',
            name='student_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='db_subjects',
            name='student_prn_no',
            field=models.CharField(max_length=100, null=True),
        ),
    ]