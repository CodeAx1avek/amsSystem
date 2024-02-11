from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Faculty(models.Model):
    faculty_id = models.CharField(max_length=10, default="")
    name = models.CharField(max_length=32, default="")

    def __str__(self):
        return self.name

class Subject(models.Model):
    subject_id = models.CharField(max_length=10, default="")
    subject_name = models.CharField(max_length=32, default="")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject_name


class DailyTimeTable(models.Model):
    period1 = models.OneToOneField(Subject, related_name='period1', on_delete=models.CASCADE)
    period2 = models.OneToOneField(Subject, related_name='period2', on_delete=models.CASCADE)
    period3 = models.OneToOneField(Subject, related_name='period3', on_delete=models.CASCADE)
    period4 = models.OneToOneField(Subject, related_name='period4', on_delete=models.CASCADE)
    period5 = models.OneToOneField(Subject, related_name='period5', on_delete=models.CASCADE)



class WeeklyTimeTable(models.Model):
    monday = models.OneToOneField(DailyTimeTable, related_name='monday', on_delete=models.CASCADE)
    tuesday = models.OneToOneField(DailyTimeTable, related_name='tuesday', on_delete=models.CASCADE)
    wednesday = models.OneToOneField(DailyTimeTable, related_name='wednesday', on_delete=models.CASCADE)
    thursday = models.OneToOneField(DailyTimeTable, related_name='thursday', on_delete=models.CASCADE)
    friday = models.OneToOneField(DailyTimeTable, related_name='friday', on_delete=models.CASCADE)

class Class(models.Model):
    branch = models.CharField(max_length=5, default="")
    section = models.CharField(max_length=1, default="")
    year = models.IntegerField(default=1)
    no_of_students = models.IntegerField(default=60)
    time_table = models.OneToOneField(WeeklyTimeTable, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.branch} {self.year}{self.section}"

class SubjectAttendanceTable(models.Model):
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE)
    attendance_count = models.IntegerField(default=0)

class StudentAttendanceTable(models.Model):
    subject1 = models.OneToOneField(SubjectAttendanceTable, related_name='subject1', on_delete=models.CASCADE)
    subject2 = models.OneToOneField(SubjectAttendanceTable, related_name='subject2', on_delete=models.CASCADE)
    subject3 = models.OneToOneField(SubjectAttendanceTable, related_name='subject3', on_delete=models.CASCADE)
    subject4 = models.OneToOneField(SubjectAttendanceTable, related_name='subject4', on_delete=models.CASCADE)
    subject5 = models.OneToOneField(SubjectAttendanceTable, related_name='subject5', on_delete=models.CASCADE)

class Student(models.Model):
    roll_no = models.CharField(max_length=10, default="")
    name = models.CharField(max_length=32, default="")
    section = models.ForeignKey(Class, on_delete=models.CASCADE)
    attendance = models.OneToOneField(StudentAttendanceTable, on_delete=models.CASCADE)

    def __str__(self):
        return self.roll_no