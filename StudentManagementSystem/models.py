from django.db import models
from django.contrib.auth.models import User


class Faculty(models.Model):
    faculty_id = models.CharField(max_length=10)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    faculties = models.ManyToManyField(Faculty)

    def __str__(self):
        return self.user.username

class Subject(models.Model):
    subject_id = models.CharField(max_length=10)
    subject_name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.subject_name

class Class(models.Model):
    branch = models.CharField(max_length=10)
    section = models.CharField(max_length=1)
    year = models.IntegerField()
    no_of_students = models.IntegerField()
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return f"{self.branch} {self.year}{self.section}"

class Student(models.Model):
    roll_no = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    section = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, default='Present')  # Example default value

    def __str__(self):
        return f"{self.student.name} - {self.subject.subject_name} - {self.date}"
