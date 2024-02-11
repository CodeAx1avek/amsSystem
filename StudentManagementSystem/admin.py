from django.contrib import admin
from .models import Faculty, Subject, DailyTimeTable, WeeklyTimeTable, Class, SubjectAttendanceTable, StudentAttendanceTable, Student

# Register your models here.
admin.site.register(Faculty)
admin.site.register(Subject)
admin.site.register(DailyTimeTable)
admin.site.register(WeeklyTimeTable)
admin.site.register(Class)
admin.site.register(SubjectAttendanceTable)
admin.site.register(StudentAttendanceTable)
admin.site.register(Student)