from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    subject_id = models.CharField(max_length=10, unique=True)
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return self.subject_name
    

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.user.username


class Class(models.Model):
    branch = models.CharField(max_length=10)
    section = models.CharField(max_length=1)
    year = models.IntegerField()
    no_of_students = models.IntegerField()
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return f"{self.branch} {self.year} - Section {self.section}"


class Student(models.Model):
    roll_no = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    section = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.name} - {self.subject.subject_name} - {self.date}"
