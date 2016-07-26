from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Faculty(models.Model):
    faculty_id = models.CharField(max_length=10,default="")
    name = models.CharField(max_length=32,default="")
    def __unicode__(self):
        return self.name

class Subject(models.Model):
    subject_id = models.CharField(max_length=10,default="")
    subject_name = models.CharField(max_length=32,default="")
    faculty = models.ForeignKey(Faculty)
    def __unicode__(self):
        return self.subject_name


class DailyTimeTable(models.Model):
    period1 = models.OneToOneField(Subject,related_name='period1')
    period2 = models.OneToOneField(Subject,related_name='period2')
    period3 = models.OneToOneField(Subject,related_name='period3')
    period4 = models.OneToOneField(Subject,related_name='period4')
    period5 = models.OneToOneField(Subject,related_name='period5')
    period6 = models.OneToOneField(Subject,related_name='period6')
    period7 = models.OneToOneField(Subject,related_name='period7')


class WeeklyTimeTable(models.Model):
    monday = models.OneToOneField(DailyTimeTable,related_name='monday')
    tuesday = models.OneToOneField(DailyTimeTable,related_name='tuesday')
    wednesday = models.OneToOneField(DailyTimeTable,related_name='wednesday')
    thursday = models.OneToOneField(DailyTimeTable,related_name='thursday')
    friday = models.OneToOneField(DailyTimeTable,related_name='friday')


class Class(models.Model):
    branch = models.CharField(max_length=5,default="")
    section = models.CharField(max_length=1,default="")
    year = models.IntegerField(default=1)
    no_of_students = models.IntegerField(default=60)
    time_table = models.OneToOneField(WeeklyTimeTable)
    def __unicode__(self):
        return self.branch+" "+self.year+self.section


class SubjectAttendenceTable(models.Model):
    subject = models.OneToOneField(Subject)
    attendence_count = models.IntegerField(default=0)

class StudentAttendenceTable(models.Model):
    subject1 = models.OneToOneField(SubjectAttendenceTable,related_name='subject1')
    subject2 = models.OneToOneField(SubjectAttendenceTable,related_name='subject2')
    subject3 = models.OneToOneField(SubjectAttendenceTable,related_name='subject3')
    subject4 = models.OneToOneField(SubjectAttendenceTable,related_name='subject4')
    subject5 = models.OneToOneField(SubjectAttendenceTable,related_name='subject5')
    subject6 = models.OneToOneField(SubjectAttendenceTable,related_name='subject6')


class Student(models.Model):
    roll_no = models.CharField(max_length=10,default="")
    name = models.CharField(max_length=32,default="")
    section = models.ForeignKey(Class)
    attendence = models.OneToOneField(StudentAttendenceTable)
    def __unicode__(self):
        return self.roll_no

