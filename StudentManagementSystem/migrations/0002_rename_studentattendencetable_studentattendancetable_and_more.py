# Generated by Django 5.0.1 on 2024-02-07 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StudentManagementSystem', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StudentAttendenceTable',
            new_name='StudentAttendanceTable',
        ),
        migrations.RenameModel(
            old_name='SubjectAttendenceTable',
            new_name='SubjectAttendanceTable',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='attendence',
            new_name='attendance',
        ),
        migrations.RenameField(
            model_name='subjectattendancetable',
            old_name='attendence_count',
            new_name='attendance_count',
        ),
    ]